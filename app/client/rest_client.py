"""
Kiwoom REST API Client
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from app.core.config import get_settings
from app.core.logging import logger
from app.core.security import token_manager
from app.core.constants import (
    TR_ID_CONDITION_LIST,
    TR_ID_CONDITION_SEARCH,
    TR_ID_STOCK_PRICE,
)
from app.shared.exceptions import AuthenticationException
from .base import BaseAPIClient

settings = get_settings()


class KiwoomRestClient(BaseAPIClient):
    """Kiwoom REST API Client"""
    
    def __init__(self):
        super().__init__(base_url=settings.KIWOOM_BASE_URL)
        self.app_key = settings.KIWOOM_APP_KEY
        self.app_secret = settings.KIWOOM_APP_SECRET
    
    def _get_auth_headers(self, tr_id: str) -> Dict[str, str]:
        """
        Get authentication headers
        
        Args:
            tr_id: Transaction ID
        
        Returns:
            Headers dictionary
        """
        access_token = token_manager.get_token()
        if not access_token:
            raise AuthenticationException("No valid access token")
        
        return {
            "authorization": f"Bearer {access_token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": tr_id,
            "custtype": "P",  # 개인
        }
    
    async def get_access_token(self) -> str:
        """
        Get OAuth access token

        Returns:
            Access token

        Raises:
            AuthenticationException: On authentication failure
        """
        logger.info("Requesting access token...")

        try:
            response = await self.post(
                "/oauth2/token",
                json={
                    "grant_type": "client_credentials",
                    "appkey": self.app_key,
                    "secretkey": self.app_secret,  # Fixed: Changed from 'appsecret' to 'secretkey'
                }
            )

            # Kiwoom API response format:
            # {'return_code': 0, 'return_msg': '정상적으로 처리되었습니다',
            #  'token': 'R22y0dDGXM...', 'token_type': 'Bearer',
            #  'expires_dt': '20251109235445'}
            
            return_code = response.get("return_code")
            if return_code != 0:
                error_msg = response.get("return_msg", "Unknown error")
                raise AuthenticationException(f"Token request failed: {error_msg} (code: {return_code})")
            
            access_token = response.get("token")  # Kiwoom uses 'token' not 'access_token'
            expires_dt_str = response.get("expires_dt")  # Format: '20251109235445' (YYYYMMDDHHmmss)
            
            if not access_token:
                raise AuthenticationException("No token in response")
            
            # Calculate expires_in from expires_dt
            if expires_dt_str:
                try:
                    expires_dt = datetime.strptime(expires_dt_str, "%Y%m%d%H%M%S")
                    now = datetime.now()
                    expires_in = int((expires_dt - now).total_seconds())
                    if expires_in < 0:
                        expires_in = 86400  # Default to 24 hours if already expired
                except Exception as e:
                    logger.warning(f"Failed to parse expires_dt '{expires_dt_str}': {e}")
                    expires_in = 86400  # Default 24 hours
            else:
                expires_in = 86400  # Default 24 hours
            
            # Store token
            token_manager.set_token(access_token, expires_in)
            
            logger.info(
                f"Access token acquired: "
                f"expires_at={expires_dt_str if expires_dt_str else 'N/A'}, "
                f"remaining={expires_in}s, "
                f"msg={response.get('return_msg', '')}"
            )
            
            return access_token
            
        except Exception as e:
            logger.error(f"Failed to get access token: {e}")
            raise AuthenticationException(f"Token acquisition failed: {e}")
    
    async def ensure_authenticated(self):
        """Ensure valid access token exists"""
        if not token_manager.is_token_valid():
            await self.get_access_token()
    
    async def get_condition_list(self) -> Dict[str, Any]:
        """
        Get list of registered condition searches
        
        Returns:
            Condition list response
        """
        await self.ensure_authenticated()
        
        logger.info("Fetching condition list...")
        
        headers = self._get_auth_headers(TR_ID_CONDITION_LIST)
        
        response = await self.get(
            "/uapi/domestic-stock/v1/quotations/psearch-result",
            headers=headers,
        )
        
        return response
    
    async def search_by_condition(
        self,
        user_id: str,
        seq: str,
    ) -> Dict[str, Any]:
        """
        Execute condition search
        
        Args:
            user_id: User ID
            seq: Condition sequence number
        
        Returns:
            Search results
        """
        await self.ensure_authenticated()
        
        logger.info(f"Executing condition search (seq: {seq})...")
        
        headers = self._get_auth_headers(TR_ID_CONDITION_SEARCH)
        
        params = {
            "user_id": user_id,
            "seq": seq,
        }
        
        response = await self.get(
            "/uapi/domestic-stock/v1/quotations/psearch-result",
            headers=headers,
            params=params,
        )
        
        return response
    
    async def get_stock_price(
        self,
        stock_code: str,
        market_code: str = "J",
    ) -> Dict[str, Any]:
        """
        Get current stock price
        
        Args:
            stock_code: 6-digit stock code
            market_code: Market code (J: KOSPI, Q: KOSDAQ)
        
        Returns:
            Stock price data
        """
        await self.ensure_authenticated()

        logger.debug(f"Fetching stock price for {stock_code}...")

        headers = self._get_auth_headers(TR_ID_STOCK_PRICE)

        params = {
            "FID_COND_MRKT_DIV_CODE": market_code,
            "FID_INPUT_ISCD": stock_code,
        }

        response = await self.get(
            "/uapi/domestic-stock/v1/quotations/inquire-price",
            headers=headers,
            params=params,
        )

        return response
