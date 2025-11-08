"""
Base exception classes
"""


class KiwoomException(Exception):
    """Base exception for Kiwoom application"""
    
    def __init__(self, message: str, code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)
