"""
Authentication API endpoints
"""

from fastapi import APIRouter, HTTPException

from app.core.logging import logger
from .service import AuthService
from .schemas import TokenResponse, TokenStatus

router = APIRouter(prefix="/auth", tags=["Authentication"])

auth_service = AuthService()


@router.post("/token", response_model=TokenResponse)
async def get_token():
    """
    Get OAuth access token
    
    Returns:
        Access token and expiration information
    """
    try:
        return await auth_service.get_token()
    except Exception as e:
        logger.error(f"Token acquisition failed: {e}")
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/token/status", response_model=TokenStatus)
async def get_token_status():
    """
    Get current token status
    
    Returns:
        Token validity and expiration status
    """
    try:
        return await auth_service.get_token_status()
    except Exception as e:
        logger.error(f"Failed to get token status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/token/refresh", response_model=TokenResponse)
async def refresh_token():
    """
    Refresh access token
    
    Returns:
        New access token
    """
    try:
        return await auth_service.refresh_token()
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        raise HTTPException(status_code=401, detail=str(e))
