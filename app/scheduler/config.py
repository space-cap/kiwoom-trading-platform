"""
Scheduler configuration
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


def create_scheduler() -> AsyncIOScheduler:
    """
    Create and configure scheduler
    
    Returns:
        Configured scheduler instance
    """
    scheduler = AsyncIOScheduler(
        timezone="Asia/Seoul",
        job_defaults={
            'coalesce': True,  # Combine multiple pending executions into one
            'max_instances': 1,  # Only one instance of job at a time
            'misfire_grace_time': 30,  # Allow 30s grace time for misfired jobs
        }
    )
    
    logger.info("Scheduler created")
    
    return scheduler
