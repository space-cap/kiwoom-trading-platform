"""
API-related exceptions
"""

from .base import KiwoomException


class APIException(KiwoomException):
    """Base API exception"""
    
    def __init__(self, message: str, status_code: int = 500, code: str = "API_ERROR"):
        self.status_code = status_code
        super().__init__(message, code)


class AuthenticationException(APIException):
    """Authentication failed exception"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401, code="AUTH_ERROR")


class RateLimitException(APIException):
    """Rate limit exceeded exception"""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429, code="RATE_LIMIT_ERROR")


class InvalidRequestException(APIException):
    """Invalid request exception"""
    
    def __init__(self, message: str = "Invalid request"):
        super().__init__(message, status_code=400, code="INVALID_REQUEST")


class ResourceNotFoundException(APIException):
    """Resource not found exception"""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, code="NOT_FOUND")
