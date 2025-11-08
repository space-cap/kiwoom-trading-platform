"""
Development environment configuration
"""

from .base import Settings


class DevSettings(Settings):
    """Development settings"""
    
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "DEBUG"
