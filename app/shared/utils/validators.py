"""
Validation utility functions
"""

import re
from typing import Optional


def validate_stock_code(stock_code: str) -> bool:
    """
    Validate Korean stock code format
    
    Args:
        stock_code: 6-digit stock code
    
    Returns:
        True if valid
    """
    return bool(re.match(r"^\d{6}$", stock_code))


def validate_market_code(market_code: str) -> bool:
    """
    Validate market code
    
    Args:
        market_code: J (KOSPI), Q (KOSDAQ), K (KONEX)
    
    Returns:
        True if valid
    """
    return market_code in ["J", "Q", "K"]


def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize string input
    
    Args:
        text: Input text
        max_length: Maximum length
    
    Returns:
        Sanitized string
    """
    text = text.strip()
    if max_length:
        text = text[:max_length]
    return text
