from sqlalchemy import Column, Integer, DateTime, JSON, func
from app.models.base import BaseModel

class Analytics(BaseModel):
    __tablename__ = 'analytics'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    metrics = Column(JSON, nullable=True) 