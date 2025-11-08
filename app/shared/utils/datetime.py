"""
DateTime utility functions
"""

from datetime import datetime, time
from typing import Optional
import pytz


KST = pytz.timezone("Asia/Seoul")


def get_kst_now() -> datetime:
    """Get current datetime in KST"""
    return datetime.now(KST)


def is_market_open(dt: Optional[datetime] = None) -> bool:
    """
    Check if market is open at given time
    
    Args:
        dt: DateTime to check (default: current time)
    
    Returns:
        True if market is open
    """
    from app.core.constants import (
        MARKET_OPEN_HOUR, MARKET_OPEN_MINUTE,
        MARKET_CLOSE_HOUR, MARKET_CLOSE_MINUTE
    )
    
    if dt is None:
        dt = get_kst_now()
    
    # Check if weekday (Monday=0, Sunday=6)
    if dt.weekday() >= 5:
        return False
    
    # Check market hours
    market_open = time(MARKET_OPEN_HOUR, MARKET_OPEN_MINUTE)
    market_close = time(MARKET_CLOSE_HOUR, MARKET_CLOSE_MINUTE)
    current_time = dt.time()
    
    return market_open <= current_time <= market_close


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string"""
    return dt.strftime(format_str)


def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """Parse string to datetime"""
    return datetime.strptime(dt_str, format_str)
