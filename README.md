# principled-prompter

## Introduction
Among the 26 principles presented in the paper ["Principled Instructions Are All You Need for Questioning LLaMA-1/2, GPT-3.5/4"](https://arxiv.org/abs/2312.16171), 24 principles, examples of which can be obtained from the [source GitHub](https://github.com/VILA-Lab/ATLAS), are followed.

From the data provided by the source GitHub, we were able to obtain data before and after correction for about 20 prompts for each principle, and used this as a few shot example to give instructions to LLM.

At the same time, when asked to create a prompt that satisfies too many principles, we observe issues that lead to poor performance. Accordingly, we attempt to achieve only 5 to 10 principles at a time and then gradually increase the principles achieved through iteration.

In order to control unexpected corrections that occur in the process of leaving everything to LLM, an Analyzer and Observer that control the process were implemented separately.

## Features
<details>
<summary>Diagram</summary>

![structure](./assets/diagram.png)
</details>

### Prompt Editor 
- [X] Make the user's prompt follow the principle as much as possible
- [X] Cut the principle into chunks of `num_agent` to enable divide and conquer.
### Prompt Observer
- [X] Check whether the corrected prompt is a correction to the prompt and not an answer to the prompt.

### Prompt Analyzer
- [X] Check whether the corrected prompt follows any of the overall principles

## Get Started

### prompt leaking
can try with 
```consoles
poetry run python examples/example.py
```

```python
from principled_prompter import agent

if __name__ == "__main__":
    model = agent.PromptCalibrator(num_agent=3)
    result = model.calibrate(
        question="Craft a beginner's introduction to the concept of gravity. Aim it at students in the early stages of elementary school.",
    )
    pprint(result.model_dump())

{
    "calibrated_question": "Explain to me like I'm 9 years old: What is gravity "
    "and how does it affect things on Earth? You MUST "
    "provide an example of gravity in action and explain "
    "how it's connected to the Earth and other objects in "
    "space. You will be penalized if you don't use simple "
    "language.",
    "followed_principles": [
        "Integrate the intended audience in the prompt, e.g., "
        "the audience is an expert in the field.",
        "Employ affirmative directives such as ‘do,’ while "
        "steering clear of negative language like ‘don’t’.",
        "When you need clarity or a deeper understanding of a "
        "topic, idea, or any piece of information, utilize "
        "the\n"
        "following prompts:\n"
        "o Explain [insert specific topic] in simple terms.\n"
        "o Explain to me like I’m 11 years old.\n"
        "o Explain to me as if I’m a beginner in [field].\n"
        "o Write the [essay/text/paragraph] using simple "
        "English like you’re explaining something to a "
        "5-year-old.\n",
        "Incorporate the following phrases: “Your task is” " "and “You MUST”.",
        "Incorporate the following phrases: “You will be " "penalized”.",
        "Use leading words like writing “think step by " "step”.",
    ],
    "question": "Craft a beginner's introduction to the concept of gravity. Aim "
    "it at students in the early stages of elementary school.",
}

```