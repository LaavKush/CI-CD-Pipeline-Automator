from .llm_client import LLMClient
from .prompt_templates import CI_GENERATION_TEMPLATE

class CIGenerator:
    def __init__(self):
        self.llm = LLMClient()

    def generate(self, project_info: dict) -> str:
        prompt = CI_GENERATION_TEMPLATE.format(context=str(project_info))
        return self.llm.ask(prompt)
