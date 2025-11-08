"""
Authentication schemas
"""

from datetime import datetime
from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    expires_at: datetime


class TokenStatus(BaseModel):
    """Token status schema"""
    is_valid: bool
    expires_at: datetime | None = None
    remaining_seconds: int | None = None
