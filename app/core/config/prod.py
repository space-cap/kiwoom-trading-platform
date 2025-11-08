"""
Production environment configuration
"""

from .base import Settings


class ProdSettings(Settings):
    """Production settings"""
    
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"
