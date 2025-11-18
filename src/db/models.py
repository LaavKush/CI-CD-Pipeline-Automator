from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    repo_url = Column(String, index=True)
    status = Column(String)
    log_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
