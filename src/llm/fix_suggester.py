from .llm_client import LLMClient

class FixSuggester:
    def __init__(self):
        self.llm = LLMClient()

    def suggest_fixes(self, error_message: str) -> str:
        """
        Takes an error message/log and returns recommended fixes.
        """

        prompt = f"""
You are an expert DevOps + CI/CD troubleshooting assistant.

Analyze the following error message or build failure log:

ERROR:
{error_message}

Provide:
- What caused the issue  
- Exact error line(s)  
- Step likely failing  
- How to fix it (actionable steps)
- Commands/config changes if needed  

Respond clearly and concisely.
"""

        return self.llm.ask(prompt)
