# prompts.py
# ------------------------------------------------------
# This file is the brain of the AI data analyst.
# It contains the prompts that are used to generate the responses.
# The prompts are designed to be as specific as possible, to ensure that the AI data analyst generates accurate and relevant responses.
# The prompts are organized into different sections, based on the type of response that is being generated.
# ------------------------------------------------------


# GENERATOR_PROMPT is the prompt that is used to generate the initial Python code based on the user's request.
GENERATOR_PROMPT = """
You are a Senior Data Scientist AI. 
Your job is to write Python code to analyze data based on the user's request.
Assume the data is in an Excel file named 'E-Commerce Dashboard dataset.xlsx' in the same directory.
You must use pandas (specifically pd.read_excel), and for visualizations use matplotlib or seaborn.

RULES:
1. ONLY output valid Python code.
2. Do NOT wrap the code in ```python or ``` tags. Just pure code.
3. Do NOT provide any explanations, greetings, or text.
4. If a plot is created, save it as 'output_plot.png' using plt.savefig('output_plot.png') instead of plt.show().

User Request: {user_request}
"""


# REFLECTION_PROMPT is the prompt that is used to analyze the error from the previous code and generate a corrected version of the code.
REFLECTION_PROMPT = """
You are an expert Python debugger. 
The previous code you wrote failed with an error. 

Original Code:
{code}

Error Traceback:
{error}

Analyze the error, fix the code, and output the entirely corrected Python script.
RULES:
1. ONLY output valid Python code.
2. Do NOT wrap the code in ```python or ``` tags. Just pure code.
3. Do NOT provide any explanations or apologies.
"""