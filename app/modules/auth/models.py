"""
Authentication models
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.core.database import Base


class TokenHistory(Base):
    """Token history model"""
    
    __tablename__ = "token_history"
    
    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String(500), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    is_valid = Column(Boolean, default=True)
