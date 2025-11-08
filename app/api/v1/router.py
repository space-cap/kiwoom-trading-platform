"""
API v1 Router
"""

from fastapi import APIRouter

from app.modules.auth.api import router as auth_router
from app.modules.condition.api import router as condition_router

api_router = APIRouter()

# Include module routers
api_router.include_router(auth_router)
api_router.include_router(condition_router)
