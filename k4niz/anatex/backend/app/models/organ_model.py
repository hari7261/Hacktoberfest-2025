from pydantic import BaseModel

class OrganInfo(BaseModel):
    organ: str
    description: str
    ai_explanation: str
