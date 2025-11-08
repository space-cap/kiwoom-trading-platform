"""
Base configuration settings
"""

from functools import lru_cache
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Kiwoom Trading Platform"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Kiwoom API
    KIWOOM_APP_KEY: str
    KIWOOM_APP_SECRET: str
    KIWOOM_BASE_URL: str = "https://openapi.koreainvestment.com:9443"
    KIWOOM_WEBSOCKET_URL: str = "ws://ops.koreainvestment.com:21000"
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/kiwoom.db"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # Scheduler
    SCHEDULER_ENABLED: bool = True
    CONDITION_CHECK_INTERVAL: int = 30  # seconds
    
    # Notification
    SLACK_WEBHOOK_URL: Optional[str] = None
    EMAIL_ENABLED: bool = False
    EMAIL_SMTP_HOST: Optional[str] = None
    EMAIL_SMTP_PORT: Optional[int] = None
    EMAIL_USERNAME: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None
    EMAIL_FROM: Optional[str] = None
    EMAIL_TO: Optional[str] = None
    
    @field_validator('EMAIL_SMTP_PORT', mode='before')
    @classmethod
    def validate_email_port(cls, v):
        """Validate email port - convert empty string to None"""
        if v == '' or v is None:
            return None
        return int(v)
    
    @field_validator('SLACK_WEBHOOK_URL', 'EMAIL_SMTP_HOST', 'EMAIL_USERNAME', 
                     'EMAIL_PASSWORD', 'EMAIL_FROM', 'EMAIL_TO', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        """Convert empty string to None"""
        if v == '':
            return None
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
