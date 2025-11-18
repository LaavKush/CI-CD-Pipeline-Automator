from typing import Optional
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    repo_url: str


class AnalyzeResponse(BaseModel):
    language: str
    framework: Optional[str] = None
    test_runner: Optional[str] = None
    hasDockerfile: bool
    context_json: dict
