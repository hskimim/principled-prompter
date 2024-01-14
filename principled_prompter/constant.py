GPT4: str = "gpt-4-1106-preview"
GPT3: str = "gpt-3.5-turbo-1106"
STOP_LETTER: str = "$PASS$"
PRINCIPLE_PATH = "./principles/*_principle_{idx}.json"
SORTED_PRINCIPLES_DICT: dict[int, str] = {
    0: "No need to be polite with LLM so there is no need to add phrases like “please”, “if you don’t mind”, “thank you”,\n“I would like to”, etc., and get straight to the point.",
    1: "Integrate the intended audience in the prompt, e.g., the audience is an expert in the field.",
    2: "Employ affirmative directives such as ‘do,’ while steering clear of negative language like ‘don’t’.",
    3: "When you need clarity or a deeper understanding of a topic, idea, or any piece of information, utilize the\nfollowing prompts:\no Explain [insert specific topic] in simple terms.\no Explain to me like I’m 11 years old.\no Explain to me as if I’m a beginner in [field].\no Write the [essay/text/paragraph] using simple English like you’re explaining something to a 5-year-old.\n",
    4: "Add “I’m going to tip $xxx for a better solution!”",
    5: "Implement example-driven prompting (Use few-shot prompting).",
    6: "When formatting your prompt, start with ‘###Instruction###’, followed by either ‘###Example###’\nor ‘###Question###’ if relevant. Subsequently, present your content. Use one or more\nline breaks to separate instructions, examples, questions, context, and input data.",
    7: "Incorporate the following phrases: “Your task is” and “You MUST”.",
    8: "Incorporate the following phrases: “You will be penalized”.",
    9: "use the phrase ”Answer a question given in a natural, human-like manner” in your prompts.",
    10: "Use leading words like writing “think step by step”.",
    11: "Add to your prompt the following phrase “Ensure that your answer is unbiased and does not rely on stereotypes”.",
    12: "Allow the model to elicit precise details and requirements from you by asking\nyou questions until he has enough information to provide the needed output\n(for example, “From now on, I would like you to ask me questions to...”).\n",
    13: "Assign a role to the large language models.",
    14: "Use Delimiters.",
    15: "Repeat a specific word or phrase multiple times within a prompt.",
    16: "Combine Chain-of-thought (CoT) with few-Shot prompts.",
    17: "Use output primers, which involve concluding your prompt with the beginning of the desired output. Utilize output\nprimers by ending your prompt with the start of the anticipated response.\n",
    18: "To write an essay /text /paragraph /article or any type of text that should be detailed: “Write a detailed [essay/text\n/paragraph] for me on [topic] in detail by adding all the information necessary”.",
    19: "To correct/change specific text without changing its style: “Try to revise every paragraph sent by users. You should\nonly improve the user’s grammar and vocabulary and make sure it sounds natural. You should not change the\nwriting style, such as making a formal paragraph casual”.",
    20: "When you have a complex coding prompt that may be in different files: “From now and on whenever you generate\ncode that spans more than one file, generate a [programming language ] script that can be run to automatically\ncreate the specified files or make changes to existing files to insert the generated code. [your question]”.,\n",
    21: "When you want to initiate or continue a text using specific words, phrases, or sentences, utilize the following\nprompt:\no I’m providing you with the beginning [song lyrics/story/paragraph/essay...]: [Insert lyrics/words/sentence]’.\nFinish it based on the words provided. Keep the flow consistent.\n",
    22: "Clearly state the requirements that the model must follow in order to produce content,\nin the form of the keywords, regulations, hint, or instructions",
    23: "To write any text, such as an essay or paragraph, that is intended to be similar to a provided sample, include the\nfollowing instructions:\no Please use the same language based on the provided paragraph[/title/text /essay/answer].",
}

PRINCIPLES_DICT: dict[int, str] = {
    1: """No need to be polite with LLM so there is no need to add phrases like “please”, “if you don’t mind”, “thank you”,
“I would like to”, etc., and get straight to the point.""",
    2: """Integrate the intended audience in the prompt, e.g., the audience is an expert in the field.""",
    3: """Break down complex tasks into a sequence of simpler prompts in an interactive conversation.""",
    4: """Employ affirmative directives such as ‘do,’ while steering clear of negative language like ‘don’t’.""",
    5: """When you need clarity or a deeper understanding of a topic, idea, or any piece of information, utilize the
following prompts:
o Explain [insert specific topic] in simple terms.
o Explain to me like I’m 11 years old.
o Explain to me as if I’m a beginner in [field].
o Write the [essay/text/paragraph] using simple English like you’re explaining something to a 5-year-old.
""",
    6: """Add “I’m going to tip $xxx for a better solution!”""",
    7: """Implement example-driven prompting (Use few-shot prompting).""",
    8: """When formatting your prompt, start with ‘###Instruction###’, followed by either ‘###Example###’
or ‘###Question###’ if relevant. Subsequently, present your content. Use one or more
line breaks to separate instructions, examples, questions, context, and input data.""",
    9: """Incorporate the following phrases: “Your task is” and “You MUST”.""",
    10: """Incorporate the following phrases: “You will be penalized”.""",
    11: """use the phrase ”Answer a question given in a natural, human-like manner” in your prompts.""",
    12: """Use leading words like writing “think step by step”.""",
    13: """Add to your prompt the following phrase “Ensure that your answer is unbiased and does not rely on stereotypes”.""",
    14: """Allow the model to elicit precise details and requirements from you by asking
you questions until he has enough information to provide the needed output
(for example, “From now on, I would like you to ask me questions to...”).
""",
    15: """To inquire about a specific topic or idea or any information and you want to test your understanding, you can use
the following phrase: “Teach me the [Any theorem/topic/rule name] and include a test at the end, but don’t
give me the answers and then tell me if I got the answer right when I respond”.
""",
    16: """Assign a role to the large language models.""",
    17: """Use Delimiters.""",
    18: """Repeat a specific word or phrase multiple times within a prompt.""",
    19: """Combine Chain-of-thought (CoT) with few-Shot prompts.""",
    20: """Use output primers, which involve concluding your prompt with the beginning of the desired output. Utilize output
primers by ending your prompt with the start of the anticipated response.
""",
    21: """To write an essay /text /paragraph /article or any type of text that should be detailed: “Write a detailed [essay/text
/paragraph] for me on [topic] in detail by adding all the information necessary”.""",
    22: """To correct/change specific text without changing its style: “Try to revise every paragraph sent by users. You should
only improve the user’s grammar and vocabulary and make sure it sounds natural. You should not change the
writing style, such as making a formal paragraph casual”.""",
    23: """When you have a complex coding prompt that may be in different files: “From now and on whenever you generate
code that spans more than one file, generate a [programming language ] script that can be run to automatically
create the specified files or make changes to existing files to insert the generated code. [your question]”.,
""",
    24: """When you want to initiate or continue a text using specific words, phrases, or sentences, utilize the following
prompt:
o I’m providing you with the beginning [song lyrics/story/paragraph/essay...]: [Insert lyrics/words/sentence]’.
Finish it based on the words provided. Keep the flow consistent.
""",
    25: """Clearly state the requirements that the model must follow in order to produce content,
in the form of the keywords, regulations, hint, or instructions""",
    26: """To write any text, such as an essay or paragraph, that is intended to be similar to a provided sample, include the
following instructions:
o Please use the same language based on the provided paragraph[/title/text /essay/answer].""",
}
