class LLMClient:
    def __init__(self, api_key:str):
        self.api_key = api_key
    def generate(self, prompt:str):
        return 'generated text'
