"""
Start standalone scheduler
"""

import asyncio
import signal
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.logging import logger
from app.core.database import init_db
from app.scheduler.config import create_scheduler
from app.scheduler.jobs import start_scheduler, stop_scheduler


async def main():
    """Main function"""
    logger.info("="*60)
    logger.info("Starting Kiwoom Trading Platform Scheduler")
    logger.info("="*60)
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return
    
    # Create and start scheduler
    scheduler = create_scheduler()
    
    def signal_handler(signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        stop_scheduler(scheduler)
        sys.exit(0)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start scheduler
    start_scheduler(scheduler)
    
    logger.info("Scheduler is running. Press Ctrl+C to stop.")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        stop_scheduler(scheduler)


if __name__ == "__main__":
    asyncio.run(main())
