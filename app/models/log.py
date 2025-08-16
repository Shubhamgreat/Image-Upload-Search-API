from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
import datetime

class APILog(Base):
    __tablename__ = "api_logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    details = Column(String)
