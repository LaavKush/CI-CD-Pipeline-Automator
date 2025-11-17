from fastapi import HTTPException

class GitHubError(HTTPException):
    def __init__(self, detail="GitHub API Error"):
        super().__init__(status_code=500, detail=detail)

class LLMError(HTTPException):
    def __init__(self, detail="LLM Processing Error"):
        super().__init__(status_code=500, detail=detail)
