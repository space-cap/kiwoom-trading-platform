"""
Authentication service
"""

from datetime import datetime, timedelta
from typing import Optional

from app.core.logging import logger
from app.core.security import token_manager
from app.client.rest_client import KiwoomRestClient
from .schemas import TokenResponse, TokenStatus


class AuthService:
    """Authentication service"""
    
    def __init__(self):
        self.client = KiwoomRestClient()
    
    async def get_token(self) -> TokenResponse:
        """
        Get access token
        
        Returns:
            TokenResponse with token details
        """
        logger.info("Getting access token...")
        
        async with self.client:
            access_token = await self.client.get_access_token()
        
        # Get token details from token manager
        expires_at = datetime.now() + timedelta(seconds=86400)  # Default 24 hours
        
        return TokenResponse(
            access_token=access_token,
            token_type="Bearer",
            expires_in=86400,
            expires_at=expires_at,
        )
    
    async def get_token_status(self) -> TokenStatus:
        """
        Get current token status
        
        Returns:
            TokenStatus with validity information
        """
        is_valid = token_manager.is_token_valid()
        
        if not is_valid:
            return TokenStatus(is_valid=False)
        
        # Calculate remaining time
        # Note: This is a simplified version. In production, you'd store expires_at
        return TokenStatus(
            is_valid=True,
            expires_at=datetime.now() + timedelta(hours=24),
            remaining_seconds=86400,
        )
    
    async def refresh_token(self) -> TokenResponse:
        """
        Refresh access token
        
        Returns:
            New TokenResponse
        """
        logger.info("Refreshing access token...")
        
        # Clear old token
        token_manager.clear_token()
        
        # Get new token
        return await self.get_token()
