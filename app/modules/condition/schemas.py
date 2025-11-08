"""
Condition search schemas
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ConditionBase(BaseModel):
    """Base condition schema"""
    seq: str
    name: str
    description: Optional[str] = None
    is_active: bool = True


class ConditionCreate(ConditionBase):
    """Create condition schema"""
    pass


class ConditionResponse(ConditionBase):
    """Condition response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SearchResultBase(BaseModel):
    """Base search result schema"""
    stock_code: str = Field(..., min_length=6, max_length=6)
    stock_name: str
    current_price: Optional[int] = None
    change_rate: Optional[float] = None
    volume: Optional[int] = None


class SearchResultResponse(SearchResultBase):
    """Search result response schema"""
    id: int
    condition_id: int
    is_new_entry: bool
    searched_at: datetime
    
    class Config:
        from_attributes = True


class ConditionSearchRequest(BaseModel):
    """Condition search request schema"""
    user_id: str
    seq: str


class ConditionSearchResponse(BaseModel):
    """Condition search response schema"""
    condition_seq: str
    condition_name: str
    total_count: int
    new_entry_count: int
    results: List[SearchResultResponse]
    searched_at: datetime


class MonitoringHistoryResponse(BaseModel):
    """Monitoring history response schema"""
    id: int
    condition_id: int
    execution_time: datetime
    result_count: int
    new_entry_count: int
    status: str
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True
