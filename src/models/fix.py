from pydantic import BaseModel


class FixRequest(BaseModel):
    apply: bool
