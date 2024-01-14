import os
import sys
from pprint import pprint

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from principled_prompter import agent  # noqa: E402

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
