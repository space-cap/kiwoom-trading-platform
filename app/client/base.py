"""
Base API Client
"""

import asyncio
import time
from typing import Optional, Dict, Any
import httpx

from app.core.config import get_settings
from app.core.logging import logger
from app.core.constants import MIN_REQUEST_INTERVAL
from app.shared.exceptions import APIException, RateLimitException

settings = get_settings()


class BaseAPIClient:
    """Base class for API clients with rate limiting and error handling"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or settings.KIWOOM_BASE_URL
        self._client: Optional[httpx.AsyncClient] = None
        self._last_request_time: float = 0
        self._request_count: int = 0
        self._rate_limit_lock = asyncio.Lock()
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_client()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def _ensure_client(self):
        """Ensure HTTP client is initialized"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(30.0),
                follow_redirects=True,
            )
    
    async def close(self):
        """Close HTTP client"""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def _wait_for_rate_limit(self):
        """Wait to comply with rate limiting"""
        async with self._rate_limit_lock:
            current_time = time.time()
            time_since_last_request = current_time - self._last_request_time
            
            if time_since_last_request < MIN_REQUEST_INTERVAL:
                wait_time = MIN_REQUEST_INTERVAL - time_since_last_request
                logger.debug(f"Rate limiting: waiting {wait_time:.3f}s")
                await asyncio.sleep(wait_time)
            
            self._last_request_time = time.time()
            self._request_count += 1
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request with rate limiting and error handling
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            headers: Request headers
            params: Query parameters
            json: JSON body
            data: Form data
        
        Returns:
            Response JSON
        
        Raises:
            APIException: On API errors
            RateLimitException: On rate limit errors
        """
        await self._ensure_client()
        await self._wait_for_rate_limit()
        
        url = endpoint if endpoint.startswith("http") else f"{self.base_url}{endpoint}"
        
        logger.debug(f"API Request: {method} {url}")
        
        try:
            response = await self._client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
                data=data,
            )
            
            # Check for rate limiting
            if response.status_code == 429:
                logger.warning("Rate limit exceeded")
                raise RateLimitException()
            
            # Log response
            logger.debug(f"API Response: {response.status_code}")
            
            # Raise for HTTP errors
            response.raise_for_status()
            
            # Parse JSON response
            return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise APIException(
                message=f"HTTP {e.response.status_code}: {e.response.text}",
                status_code=e.response.status_code,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise APIException(message=f"Request failed: {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            raise APIException(message=f"Unexpected error: {str(e)}")
    
    async def get(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make GET request"""
        return await self._request("GET", endpoint, headers=headers, params=params)
    
    async def post(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make POST request"""
        return await self._request("POST", endpoint, headers=headers, json=json, data=data)
