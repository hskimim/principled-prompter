import logging
import random
from collections import Counter
from copy import copy
from glob import glob

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from tqdm import tqdm

from principled_prompter import constant, prompts, utils
from principled_prompter.schemas import (
    CalibratedPrompt,
    FewShotSamplesAboutPrinciples,
    Principles,
)

load_dotenv(verbose=True)
logging.basicConfig(level=logging.DEBUG)


class OpenAIModel:
    def __init__(self) -> None:
        self._client = OpenAI()


class Analyzer(OpenAIModel):
    def run(
        self,
        question: str,
        corrected: str,
        vote_threshold: int = 5,
    ) -> list[int]:
        msg = [
            {
                "role": "user",
                "content": prompts.ANALYZER_PROMPT.format(
                    prompt_dict=constant.SORTED_PRINCIPLES_DICT,
                    before_prompt=question,
                    after_prompt=corrected,
                ),
            }
        ]

        monitor = self._client.chat.completions.create(
            model=constant.GPT4,
            messages=msg,  # type:ignore
            temperature=1,
            n=30,
        )

        votes = [
            choice.message.content
            for choice in monitor.choices
            if choice.message.content is not None
        ]
        try:
            nested_ls: list[list[int]] = []
            for str_ in votes:
                try:
                    ls = eval(str_)
                    if isinstance(ls, list) and isinstance(ls[0], int):
                        nested_ls.append(ls)
                except Exception:
                    continue
            vote_dict = Counter([j for i in nested_ls for j in i])
        except Exception:
            print(votes)
            # error during eval()
            raise ValueError
        considered_principles = [k for k, v in vote_dict.items() if v > vote_threshold]
        return considered_principles


class Observer(OpenAIModel):
    def run(self, question: str, corrected: str) -> str:
        msg = [
            {
                "role": "user",
                "content": prompts.MONITOR_PROMPT.format(
                    prompt=question, answer=corrected
                ),
            }
        ]
        monitor = self._client.chat.completions.create(
            model=constant.GPT4,
            messages=msg,  # type:ignore
            temperature=1,
            n=100,
        )

        votes = [choice.message.content for choice in monitor.choices]
        vote_dict = Counter(votes)
        relation = max(vote_dict.items(), key=lambda x: x[1])[0]

        if relation not in {"QA", "CORRECTION"}:
            raise ValueError
        return relation


class Editor(OpenAIModel):
    def __init__(self, num_few_shot_examples: int = 5) -> None:
        super().__init__()
        self._principles = self._load_principles_from_files()
        if len(self._principles) != 24:
            raise ValueError("please check the PRINCIPLE_PATH in constant.py")

        self.num_few_shot_examples = num_few_shot_examples

    def _load_principles_from_files(self) -> list[Principles]:
        principles = []

        for idx in range(1, 26 + 1):
            paths = sorted(glob(constant.PRINCIPLE_PATH.format(idx=idx)))

            if len(paths) != 2:
                continue

            after_principle, before_principle = paths

            after = utils.extract_instruction_from_json(
                utils.read_json(after_principle)
            )
            before = utils.extract_instruction_from_json(
                utils.read_json(before_principle)
            )

            result = [
                FewShotSamplesAboutPrinciples(before_principle=b, after_principle=a)
                for b, a in list(zip(before, after))
            ]
            principles.append(
                Principles(
                    advice=constant.PRINCIPLES_DICT[idx], few_shot_samples=result
                )
            )
        return principles

    def _prepare_few_shot_examples_prompt(self, principle: Principles) -> list[str]:
        few_shot_exs: list[str] = [
            "From now on, I will show several examples of prompt corrections according to the principle."
        ]

        for example in principle.few_shot_samples:
            formatted_prompt = prompts.FEW_SHOT_PROMPT.format(
                before_principle=example.before_principle,
                after_principle=example.after_principle,
            )
            few_shot_exs.append(formatted_prompt)
        return few_shot_exs

    def _add_principle_prompts(
        self,
        principle: Principles,
    ) -> list[ChatCompletionSystemMessageParam]:
        sys_prompt = [
            ChatCompletionSystemMessageParam(
                role="system",
                content=prompts.PRINCIPLE_PROMPT.format(principle=principle.advice),
            )
        ] + [
            ChatCompletionSystemMessageParam(role="system", content=prompt)
            for prompt in self._prepare_few_shot_examples_prompt(principle)[
                : self.num_few_shot_examples
            ]
        ]
        return sys_prompt

    def _generate_system_prompt_for_single_agent(
        self, principles: list[Principles], persona: str
    ) -> list[ChatCompletionSystemMessageParam]:
        system_prompt: list[ChatCompletionSystemMessageParam] = [
            ChatCompletionSystemMessageParam(role="system", content=persona)
        ]
        for principle in principles:
            system_prompt += self._add_principle_prompts(principle)
        return system_prompt

    def _generate_system_prompt(
        self, question: str, principles: list[Principles], persona: str
    ) -> list[ChatCompletionUserMessageParam | ChatCompletionSystemMessageParam]:
        return self._generate_system_prompt_for_single_agent(principles, persona) + [
            ChatCompletionUserMessageParam(role="user", content=question)
        ]

    def run(
        self,
        prompt: str,
        principle_indices: list[int],
        memory: list[int] | None = None,
    ) -> str:
        msg = self._generate_system_prompt(
            question=prompt,
            principles=[
                principle
                for idx, principle in enumerate(self._principles)
                if idx in principle_indices
            ],
            persona=prompts.INIT_PERSONA
            if memory is None
            else prompts.MEMORY_PERSONA.format(
                FULFILLED_PRINCIPLE_LIST=[
                    principle.advice
                    for idx, principle in enumerate(self._principles)
                    if idx in memory
                ]
            ),
        )

        answer = self._client.chat.completions.create(
            model=constant.GPT3,
            messages=msg,  # type:ignore
            temperature=1,
            n=30,
        )
        return [
            choice.message.content
            for choice in answer.choices
            if choice.message.content is not None
        ][0]


class PromptCalibrator(OpenAIModel):
    def __init__(self, num_agent: int = 5) -> None:
        """
        num_agent :
            Instead of allowing many principles to be achieved at once,
            principles as many as 24//num_agent are allocated and principles are achieved in batch units.
        """
        self._editor = Editor()
        self._analyzer = Analyzer()
        self._observer = Observer()
        self._num_agent = num_agent

    @staticmethod
    def _draw_index(end_index) -> int:
        return random.randint(a=0, b=end_index)

    def calibrate(
        self,
        question: str,
        iters: int = 10,
        verbose: bool = True,
    ) -> CalibratedPrompt:
        """
        question :
            Prompt you want to correct
        iters :
            Number of iterations of calibration
        verbose :
            If True, you can see that the progress bar and prompt of the iteration are being corrected.
        """
        before_score = 0
        memory = None
        chunks = utils.split_list(
            list(range(1, len(self._editor._principles) + 1)), self._num_agent
        )
        prompt = copy(question)

        for _ in tqdm(range(iters)) if verbose else range(iters):  # type:ignore
            agent_index = self._draw_index(len(chunks) - 1)
            corrected = self._editor.run(
                prompt=prompt, principle_indices=chunks[agent_index], memory=memory
            )
            analyzed = self._analyzer.run(question=prompt, corrected=corrected)
            observed = self._observer.run(question=prompt, corrected=corrected)
            score = len(analyzed)

            if observed == "CORRECTION" and before_score < score:
                if verbose:
                    logging.debug(f"{prompt} \n -> \n {corrected}")
                prompt = corrected
                before_score = len(analyzed)
                memory = analyzed
                try:
                    description = [
                        self._editor._principles[index].advice for index in analyzed
                    ]
                except IndexError:
                    print(analyzed)
                    print(self._editor._principles)
                    raise IndexError
        return CalibratedPrompt(
            question=question,
            calibrated_question=prompt,
            followed_principles=description,
        )
