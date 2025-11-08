"""
Scheduler job management
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from app.core.config import get_settings
from app.core.logging import logger
from .tasks import check_conditions_task, token_refresh_task

settings = get_settings()


def register_jobs(scheduler: AsyncIOScheduler):
    """
    Register all scheduled jobs
    
    Args:
        scheduler: Scheduler instance
    """
    if not settings.SCHEDULER_ENABLED:
        logger.info("Scheduler is disabled")
        return
    
    # Job 1: Check conditions periodically
    scheduler.add_job(
        check_conditions_task,
        trigger=IntervalTrigger(seconds=settings.CONDITION_CHECK_INTERVAL),
        id="check_conditions",
        name="Check condition searches",
        replace_existing=True,
    )
    logger.info(
        f"Registered job: check_conditions "
        f"(interval: {settings.CONDITION_CHECK_INTERVAL}s)"
    )
    
    # Job 2: Refresh token daily
    scheduler.add_job(
        token_refresh_task,
        trigger=CronTrigger(hour=8, minute=0),  # 8:00 AM daily
        id="refresh_token",
        name="Refresh authentication token",
        replace_existing=True,
    )
    logger.info("Registered job: refresh_token (daily at 8:00 AM)")


def start_scheduler(scheduler: AsyncIOScheduler):
    """
    Start the scheduler
    
    Args:
        scheduler: Scheduler instance
    """
    if not settings.SCHEDULER_ENABLED:
        logger.warning("Scheduler is disabled in settings")
        return
    
    register_jobs(scheduler)
    
    scheduler.start()
    logger.info("Scheduler started successfully")


def stop_scheduler(scheduler: AsyncIOScheduler):
    """
    Stop the scheduler
    
    Args:
        scheduler: Scheduler instance
    """
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
