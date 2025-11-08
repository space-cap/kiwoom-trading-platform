"""
Condition search API endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import logger
from .service import ConditionService
from .schemas import (
    ConditionResponse,
    ConditionSearchRequest,
    ConditionSearchResponse,
)

router = APIRouter(prefix="/conditions", tags=["Condition Search"])


def get_condition_service(db: Session = Depends(get_db)) -> ConditionService:
    """Get condition service instance"""
    return ConditionService(db)


@router.get("/", response_model=List[ConditionResponse])
async def get_conditions(
    active_only: bool = False,
    service: ConditionService = Depends(get_condition_service)
):
    """
    Get all conditions from database
    
    Args:
        active_only: Return only active conditions
    
    Returns:
        List of conditions
    """
    try:
        return service.get_all_conditions(active_only=active_only)
    except Exception as e:
        logger.error(f"Failed to get conditions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync", response_model=List[ConditionResponse])
async def sync_conditions(
    service: ConditionService = Depends(get_condition_service)
):
    """
    Fetch conditions from API and sync with database
    
    Returns:
        List of synced conditions
    """
    try:
        return await service.fetch_and_sync_conditions()
    except Exception as e:
        logger.error(f"Failed to sync conditions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=ConditionSearchResponse)
async def execute_condition_search(
    request: ConditionSearchRequest,
    service: ConditionService = Depends(get_condition_service)
):
    """
    Execute condition search
    
    Args:
        request: Search request with user_id and seq
    
    Returns:
        Search results with new entries highlighted
    """
    try:
        return await service.execute_condition_search(
            user_id=request.user_id,
            seq=request.seq
        )
    except Exception as e:
        logger.error(f"Condition search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
