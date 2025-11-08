"""
Console notification provider
"""

from app.core.logging import logger


class ConsoleNotificationProvider:
    """Console notification provider"""
    
    async def send(self, message: str, level: str = "info"):
        """
        Send console notification
        
        Args:
            message: Notification message
            level: Log level (info, warning, error)
        """
        if level == "error":
            logger.error(message)
        elif level == "warning":
            logger.warning(message)
        else:
            logger.info(message)
