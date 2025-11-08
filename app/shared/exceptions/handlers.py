"""
Exception handlers for FastAPI
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.logging import logger
from .base import KiwoomException
from .api_exceptions import APIException


async def kiwoom_exception_handler(request: Request, exc: KiwoomException) -> JSONResponse:
    """Handle KiwoomException"""
    logger.error(f"KiwoomException: {exc.message} (code: {exc.code})")
    
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    if isinstance(exc, APIException):
        status_code = exc.status_code
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions"""
    logger.exception(f"Unhandled exception: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred",
            }
        }
    )
