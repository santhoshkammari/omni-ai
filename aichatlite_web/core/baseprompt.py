from datetime import datetime


class BasePrompt:
    TODAY_DATE = f"""The current date is {datetime.now().strftime("%Y-%m-%d")}.\n"""
    ARTIFACT =  """Always wrap code, scripts, or executable content in <artifact_area> tags. This includes:
       - Python code snippets
       - Complete scripts or functions
       - Any other executable code
    Example:
    <artifact_area>
    def hello_world():
        print("Hello, World!")
    </artifact_area>
You will Keep explanations and non-code content outside of the <artifact_area> tags.
DO NOT FORGET TO WRAP PYTHON CODE TO WRAP IN <artifact_area> tags."""