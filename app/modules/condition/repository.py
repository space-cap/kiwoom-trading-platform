"""
Condition search repository
"""

from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.logging import logger
from .models import Condition, SearchResult, MonitoringHistory
from .schemas import ConditionCreate


class ConditionRepository:
    """Repository for condition search data"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_condition_by_seq(self, seq: str) -> Optional[Condition]:
        """Get condition by sequence number"""
        return self.db.query(Condition).filter(Condition.seq == seq).first()
    
    def get_all_conditions(self, active_only: bool = False) -> List[Condition]:
        """Get all conditions"""
        query = self.db.query(Condition)
        if active_only:
            query = query.filter(Condition.is_active == True)
        return query.all()
    
    def create_condition(self, condition_data: ConditionCreate) -> Condition:
        """Create new condition"""
        condition = Condition(**condition_data.model_dump())
        self.db.add(condition)
        self.db.commit()
        self.db.refresh(condition)
        return condition
    
    def update_condition(self, condition: Condition) -> Condition:
        """Update condition"""
        condition.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(condition)
        return condition
    
    def get_previous_results(
        self,
        condition_id: int,
        since: Optional[datetime] = None
    ) -> List[SearchResult]:
        """Get previous search results"""
        query = self.db.query(SearchResult).filter(
            SearchResult.condition_id == condition_id
        )
        
        if since:
            query = query.filter(SearchResult.searched_at >= since)
        
        return query.all()
    
    def save_search_results(
        self,
        condition_id: int,
        results: List[dict],
        previous_stock_codes: set
    ) -> List[SearchResult]:
        """Save search results"""
        saved_results = []
        
        for result_data in results:
            stock_code = result_data["stock_code"]
            is_new_entry = stock_code not in previous_stock_codes
            
            result = SearchResult(
                condition_id=condition_id,
                stock_code=stock_code,
                stock_name=result_data["stock_name"],
                current_price=result_data.get("current_price"),
                change_rate=result_data.get("change_rate"),
                volume=result_data.get("volume"),
                is_new_entry=is_new_entry,
                searched_at=datetime.now()
            )
            
            self.db.add(result)
            saved_results.append(result)
        
        self.db.commit()
        
        for result in saved_results:
            self.db.refresh(result)
        
        return saved_results
    
    def save_monitoring_history(
        self,
        condition_id: int,
        result_count: int,
        new_entry_count: int,
        status: str = "success",
        error_message: Optional[str] = None
    ) -> MonitoringHistory:
        """Save monitoring history"""
        history = MonitoringHistory(
            condition_id=condition_id,
            execution_time=datetime.now(),
            result_count=result_count,
            new_entry_count=new_entry_count,
            status=status,
            error_message=error_message
        )
        
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        
        return history
    
    def get_monitoring_history(
        self,
        condition_id: Optional[int] = None,
        limit: int = 100
    ) -> List[MonitoringHistory]:
        """Get monitoring history"""
        query = self.db.query(MonitoringHistory)
        
        if condition_id:
            query = query.filter(MonitoringHistory.condition_id == condition_id)
        
        return query.order_by(desc(MonitoringHistory.execution_time)).limit(limit).all()
