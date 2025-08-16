from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ImageBase(BaseModel):
    filename: str
    size: int
    width: int
    height: int
    upload_timestamp: datetime
    thumbnail_path: Optional[str]

class ImageCreate(BaseModel):
    filename: str
    size: int
    width: int
    height: int
    thumbnail_path: Optional[str]

class ImageOut(ImageBase):
    id: int
    class Config:
        from_attributes = True
