# from pydantic import BaseModel


# class WorkflowRequest(BaseModel):
#     repo_url: str
#     branch: str = "main"

from pydantic import BaseModel

class LogExplainRequest(BaseModel):
    log_text: str
