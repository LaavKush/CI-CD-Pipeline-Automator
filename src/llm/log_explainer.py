from .llm_client import LLMClient

class LogExplainer:
    def __init__(self):
        self.llm = LLMClient()

    def explain(self, logs: str) -> str:
        prompt = f"""
You are an AI DevOps assistant. Analyze the following CI/CD logs and explain:

- What caused the failure?
- Which step failed?
- The exact error line
- How to fix it

Logs:
{logs}

Respond in clear bullet points.
"""
        return self.llm.ask(prompt)
