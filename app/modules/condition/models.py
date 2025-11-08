"""
Condition search models
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Condition(Base):
    """Condition search model"""
    
    __tablename__ = "conditions"
    
    id = Column(Integer, primary_key=True, index=True)
    seq = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    results = relationship("SearchResult", back_populates="condition")
    monitoring_history = relationship("MonitoringHistory", back_populates="condition")


class SearchResult(Base):
    """Search result model"""
    
    __tablename__ = "search_results"
    
    id = Column(Integer, primary_key=True, index=True)
    condition_id = Column(Integer, ForeignKey("conditions.id"), nullable=False)
    stock_code = Column(String(6), index=True, nullable=False)
    stock_name = Column(String(100), nullable=False)
    current_price = Column(Integer)
    change_rate = Column(Float)
    volume = Column(Integer)
    is_new_entry = Column(Boolean, default=False)
    searched_at = Column(DateTime, default=datetime.now, nullable=False, index=True)
    
    # Relationships
    condition = relationship("Condition", back_populates="results")


class MonitoringHistory(Base):
    """Monitoring history model"""
    
    __tablename__ = "monitoring_history"
    
    id = Column(Integer, primary_key=True, index=True)
    condition_id = Column(Integer, ForeignKey("conditions.id"), nullable=False)
    execution_time = Column(DateTime, default=datetime.now, nullable=False)
    result_count = Column(Integer, default=0)
    new_entry_count = Column(Integer, default=0)
    status = Column(String(20), default="success")  # success, failed
    error_message = Column(String(500))
    
    # Relationships
    condition = relationship("Condition", back_populates="monitoring_history")
