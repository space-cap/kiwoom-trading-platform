"""
Initialize database
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import Base, engine, init_db
from app.core.logging import logger

# Import all models to ensure they are registered
from app.modules.auth.models import TokenHistory
from app.modules.condition.models import Condition, SearchResult, MonitoringHistory


def main():
    """Initialize database tables"""
    logger.info("Initializing database...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("Database tables created successfully:")
        for table in Base.metadata.sorted_tables:
            logger.info(f"  - {table.name}")
        
        logger.info("Database initialization complete!")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    main()
