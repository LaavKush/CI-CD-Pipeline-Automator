from pydantic import BaseModel

class AnalysisBase(BaseModel):
    repo_url: str
    status: str
    log_text: str

class AnalysisCreate(AnalysisBase):
    pass

class AnalysisResponse(AnalysisBase):
    id: int

    class Config:
        orm_mode = True
