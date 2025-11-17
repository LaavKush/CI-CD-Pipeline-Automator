from pydantic import BaseModel


class WorkflowRequest(BaseModel):
    repo_url: str
    branch: str = "main"
