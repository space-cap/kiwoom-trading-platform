"""
Condition search service
"""

from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.logging import logger
from app.client.rest_client import KiwoomRestClient
from .repository import ConditionRepository
from .schemas import (
    ConditionResponse,
    ConditionCreate,
    ConditionSearchResponse,
    SearchResultResponse,
)


class ConditionService:
    """Condition search service"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = ConditionRepository(db)
        self.client = KiwoomRestClient()
    
    async def fetch_and_sync_conditions(self) -> List[ConditionResponse]:
        """
        Fetch conditions from API and sync with database
        
        Returns:
            List of synced conditions
        """
        logger.info("Fetching condition list from API...")
        
        async with self.client:
            response = await self.client.get_condition_list()
        
        # Parse response (adjust based on actual API response structure)
        conditions_data = response.get("output", [])
        
        synced_conditions = []
        
        for condition_data in conditions_data:
            seq = condition_data.get("seq")
            name = condition_data.get("name", f"Condition {seq}")
            
            # Check if exists
            existing = self.repository.get_condition_by_seq(seq)
            
            if existing:
                condition = existing
            else:
                # Create new
                condition = self.repository.create_condition(
                    ConditionCreate(
                        seq=seq,
                        name=name,
                        is_active=True
                    )
                )
            
            synced_conditions.append(ConditionResponse.model_validate(condition))
        
        logger.info(f"Synced {len(synced_conditions)} conditions")
        
        return synced_conditions
    
    async def execute_condition_search(
        self,
        user_id: str,
        seq: str
    ) -> ConditionSearchResponse:
        """
        Execute condition search and save results
        
        Args:
            user_id: User ID
            seq: Condition sequence number
        
        Returns:
            Search results
        """
        logger.info(f"Executing condition search (seq: {seq})...")
        
        # Get condition from DB
        condition = self.repository.get_condition_by_seq(seq)
        if not condition:
            # Create if not exists
            condition = self.repository.create_condition(
                ConditionCreate(
                    seq=seq,
                    name=f"Condition {seq}",
                    is_active=True
                )
            )
        
        # Get previous results (last hour)
        since = datetime.now() - timedelta(hours=1)
        previous_results = self.repository.get_previous_results(condition.id, since)
        previous_stock_codes = {r.stock_code for r in previous_results}
        
        # Execute search via API
        async with self.client:
            response = await self.client.search_by_condition(user_id, seq)
        
        # Parse results (adjust based on actual API response structure)
        api_results = response.get("output", [])
        
        results_data = []
        for item in api_results:
            results_data.append({
                "stock_code": item.get("stock_code", ""),
                "stock_name": item.get("stock_name", ""),
                "current_price": item.get("current_price"),
                "change_rate": item.get("change_rate"),
                "volume": item.get("volume"),
            })
        
        # Save results
        saved_results = self.repository.save_search_results(
            condition.id,
            results_data,
            previous_stock_codes
        )
        
        # Count new entries
        new_entry_count = sum(1 for r in saved_results if r.is_new_entry)
        
        # Save monitoring history
        self.repository.save_monitoring_history(
            condition.id,
            result_count=len(saved_results),
            new_entry_count=new_entry_count,
            status="success"
        )
        
        logger.info(
            f"Search completed: {len(saved_results)} results, "
            f"{new_entry_count} new entries"
        )
        
        return ConditionSearchResponse(
            condition_seq=condition.seq,
            condition_name=condition.name,
            total_count=len(saved_results),
            new_entry_count=new_entry_count,
            results=[SearchResultResponse.model_validate(r) for r in saved_results],
            searched_at=datetime.now()
        )
    
    def get_all_conditions(self, active_only: bool = False) -> List[ConditionResponse]:
        """Get all conditions from database"""
        conditions = self.repository.get_all_conditions(active_only)
        return [ConditionResponse.model_validate(c) for c in conditions]
