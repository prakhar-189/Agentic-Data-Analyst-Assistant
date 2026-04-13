# tools.py 
# ------------------------------------------------------
# This file contains the tools that the AI data analyst uses to execute Python code and handle errors.
# The main function is execute_python_code, which takes a string of Python code, executes it, and returns the output or any errors that occur.
# This function is designed to be safe and to capture any exceptions that may arise during execution, allowing the AI data analyst to reflect on the errors and generate corrected code.
# ------------------------------------------------------


# Importing Neccessary Libraries
# ------------------------------
# Sys and io are used to redirect standard output so we can capture print statements from the executed code.
# Traceback is used to capture the full error traceback if the code execution fails, which is essential for debugging and reflection.
# ------------------------------
import sys
import io
import traceback

def execute_python_code(code: str) -> dict:
    """
    Safely executes a string of Python code and captures the output/errors.
    """
    # Clean up any markdown formatting if the LLM accidentally includes it
    clean_code = code.replace("```python", "").replace("```", "").strip()
    
    # Redirect standard output to capture print statements
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    
    try:
        # Execute the code in an isolated dictionary (namespace)
        exec(clean_code, {})
        sys.stdout = old_stdout
        output = redirected_output.getvalue()
        return {"status": "success", "output": output}
        
    except Exception as e:
        # If it crashes, capture the error so the agent can reflect on it
        sys.stdout = old_stdout
        error_msg = traceback.format_exc()
        return {"status": "error", "output": error_msg}