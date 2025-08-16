from pydantic import BaseModel
from datetime import datetime

class APILogBase(BaseModel):
    action: str
    timestamp: datetime
    details: str

class APILogOut(APILogBase):
    id: int
    class Config:
        from_attributes = True
