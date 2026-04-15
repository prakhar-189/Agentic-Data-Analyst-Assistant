# tools.py 
# ------------------------------------------------------
# This file contains the tools that the AI data analyst uses to execute Python code and handle errors.
# The main function is execute_python_code, which takes a string of Python code, executes it, and returns the output or any errors that occur.
# This function is designed to be safe and to capture any exceptions that may arise during execution, allowing the AI data analyst to reflect on the errors and generate corrected code.
# ------------------------------------------------------


# =================================================
# Importing Neccessary Libraries
# ------------------------------
# Sys and io are used to redirect standard output so we can capture print statements from the executed code.
# Traceback is used to capture the full error traceback if the code execution fails, which is essential for debugging and reflection.
# Re is used to clean the code of any markdown formatting that the LLM might have included, ensuring that we execute only the raw Python code.
# ================================================
import sys
import io
import traceback
import re



# =================================================
# sanitize_filename is a utility function that takes a string title and converts it into a safe filename format by making it lowercase, removing special characters, and replacing spaces with underscores.
# This is used to ensure that any files saved by the generated code have valid and consistent filenames.
# =================================================
def sanitize_filename(title: str) -> str:
    """
    Takes an arbitrary title and converts it to a safe,
    lowercase, and underscore-separated filename.
    """
    # 1. Convert to lowercase
    safe_name = title.lower()
    # 2. Keep only alphanumeric characters and spaces
    safe_name = re.sub(r'[^a-z0-9\s]', '', safe_name)
    # 3. Replace spaces with underscores
    safe_name = re.sub(r'\s+', '_', safe_name)
    return safe_name.strip('_')


# =================================================
# execute_python_code is a function that safely executes a string of Python code with strict guardrails.
# It first cleans the code of any markdown tags, then checks for any forbidden keywords that could pose a security risk.
# If the code passes these checks, it executes the code in an isolated memory space and captures any output or errors that occur.
# The function returns a dictionary indicating whether the execution was successful and either the output or the error
# =================================================
def execute_python_code(code: str) -> dict:
    """
    Safely executes a string of Python code with strict guardrails.
    """
    # LAYER 2: Output Constraint (Regex Filter)
    # Strip markdown tags in case the LLM ignored formatting rules
    clean_code = re.sub(r"^```python\s*", "", code, flags=re.MULTILINE)
    clean_code = re.sub(r"^```\s*", "", clean_code, flags=re.MULTILINE)
    clean_code = clean_code.strip()

    # LAYER 3: Safety Guardrails (Deny List)
    # Block any commands that could interact with your operating system
    forbidden_keywords = [
        "import os", "import sys", "import subprocess", "import shutil", 
        "os.", "sys.", "eval(", "exec(", "open("
    ]
    
    for keyword in forbidden_keywords:
        if keyword in clean_code:
            return {
                "status": "error", 
                "output": f"SecurityViolation: The use of '{keyword}' is strictly prohibited in this environment."
            }

    # The Execution Sandbox
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    
    try:
        # Run the clean, verified code in an isolated memory space
        namespace = {'sanitize_filename': sanitize_filename}
        exec(clean_code, namespace)
        sys.stdout = old_stdout
        output = redirected_output.getvalue()
        return {"status": "success", "output": output}
        
    except Exception as e:
        sys.stdout = old_stdout
        error_msg = traceback.format_exc()
        return {"status": "error", "output": error_msg}