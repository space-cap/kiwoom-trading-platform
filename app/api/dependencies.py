"""
Common API dependencies
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import token_manager


async def require_authentication():
    """
    Dependency to require valid authentication
    
    Raises:
        HTTPException: If not authenticated
    """
    if not token_manager.is_token_valid():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated or token expired",
        )


def get_db_session() -> Generator[Session, None, None]:
    """Get database session (alias for get_db)"""
    yield from get_db()
