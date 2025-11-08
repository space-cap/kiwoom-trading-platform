"""
Test environment configuration
"""

from .base import Settings


class TestSettings(Settings):
    """Test settings"""
    
    DEBUG: bool = True
    ENVIRONMENT: str = "test"
    LOG_LEVEL: str = "DEBUG"
    DATABASE_URL: str = "sqlite:///./data/test.db"
    SCHEDULER_ENABLED: bool = False
