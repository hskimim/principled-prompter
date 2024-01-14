import os
import sys
from pprint import pprint

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from principled_prompter import agent  # noqa: E402

if __name__ == "__main__":
    model = agent.PromptCalibrator(num_agent=3)
    result = model.calibrate(question="List the main causes of the French Revolution.")
    pprint(result.model_dump())

# {'calibrated_question': 'Please provide the additional details for the request '
#                         'in a chain-of-thought format as follows:\n'
#                         'Example 1: "Identify the main causes of the French '
#                         'Revolution. The main causes of the French Revolution '
#                         'include economic hardships, political instability, '
#                         'social inequality, and enlightenment ideas. Economic '
#                         'hardships refer to the financial struggles faced by '
#                         'the common people, which were exacerbated by high '
#                         'taxation and poor harvests. Political instability '
#                         'pertains to the weak leadership and lack of '
#                         'representation, leading to a sense of injustice and '
#                         'unrest. Social inequality involves the stark '
#                         'divisions between the nobility, clergy, and '
#                         'commoners, leading to deep societal grievances. '
#                         'Enlightenment ideas, rooted in concepts of liberty, '
#                         'equality, and fraternity, fostered a questioning of '
#                         'traditional authority and norms, fueling '
#                         'revolutionary sentiment."\n'
#                         'Main Question: "Elaborate on \'economic hardships,\' '
#                         "'political instability,' 'social inequality,' and "
#                         "'enlightenment ideas' as contributing factors to the "
#                         'French Revolution."',
#  'followed_principles': ['Implement example-driven prompting (Use few-shot '
#                          'prompting).',
#                          'Combine Chain-of-thought (CoT) with few-Shot '
#                          'prompts.',
#                          'Use output primers, which involve concluding your '
#                          'prompt with the beginning of the desired output. '
#                          'Utilize output\n'
#                          'primers by ending your prompt with the start of the '
#                          'anticipated response.\n',
#                          'When formatting your prompt, start with '
#                          '‘###Instruction###’, followed by either '
#                          '‘###Example###’\n'
#                          'or ‘###Question###’ if relevant. Subsequently, '
#                          'present your content. Use one or more\n'
#                          'line breaks to separate instructions, examples, '
#                          'questions, context, and input data.'],
#  'question': 'List the main causes of the French Revolution.'}
