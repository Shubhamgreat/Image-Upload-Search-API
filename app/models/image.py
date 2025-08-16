from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
import datetime

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    size = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    upload_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    thumbnail_path = Column(String)
