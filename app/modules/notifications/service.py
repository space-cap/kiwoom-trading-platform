"""
Notification service
"""

from typing import List, Optional
from datetime import datetime

from app.core.config import get_settings
from app.core.logging import logger
from app.core.constants import NOTIFICATION_CONSOLE, NOTIFICATION_SLACK, NOTIFICATION_EMAIL

settings = get_settings()


class NotificationService:
    """Notification service for sending alerts"""
    
    def __init__(self):
        self.enabled_channels = self._get_enabled_channels()
    
    def _get_enabled_channels(self) -> List[str]:
        """Get list of enabled notification channels"""
        channels = [NOTIFICATION_CONSOLE]  # Console is always enabled
        
        if settings.SLACK_WEBHOOK_URL:
            channels.append(NOTIFICATION_SLACK)
        
        if settings.EMAIL_ENABLED:
            channels.append(NOTIFICATION_EMAIL)
        
        return channels
    
    async def send_new_entry_alert(
        self,
        condition_name: str,
        stock_code: str,
        stock_name: str,
        current_price: Optional[int] = None,
        change_rate: Optional[float] = None
    ):
        """
        Send alert for new condition entry
        
        Args:
            condition_name: Name of the condition
            stock_code: Stock code
            stock_name: Stock name
            current_price: Current price
            change_rate: Change rate
        """
        message = self._format_new_entry_message(
            condition_name,
            stock_code,
            stock_name,
            current_price,
            change_rate
        )
        
        await self._send_notification(message, level="info")
    
    async def send_error_alert(self, error_message: str, context: Optional[str] = None):
        """
        Send error alert
        
        Args:
            error_message: Error message
            context: Additional context
        """
        message = f"🚨 Error: {error_message}"
        if context:
            message += f"\nContext: {context}"
        
        await self._send_notification(message, level="error")
    
    def _format_new_entry_message(
        self,
        condition_name: str,
        stock_code: str,
        stock_name: str,
        current_price: Optional[int],
        change_rate: Optional[float]
    ) -> str:
        """Format new entry notification message"""
        lines = [
            f"📈 New Stock Entry",
            f"Condition: {condition_name}",
            f"Stock: {stock_name} ({stock_code})",
        ]
        
        if current_price:
            lines.append(f"Price: {current_price:,}원")
        
        if change_rate:
            sign = "+" if change_rate > 0 else ""
            lines.append(f"Change: {sign}{change_rate:.2f}%")
        
        lines.append(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(lines)
    
    async def _send_notification(self, message: str, level: str = "info"):
        """
        Send notification to all enabled channels
        
        Args:
            message: Notification message
            level: Notification level (info, warning, error)
        """
        for channel in self.enabled_channels:
            try:
                if channel == NOTIFICATION_CONSOLE:
                    await self._send_console(message, level)
                elif channel == NOTIFICATION_SLACK:
                    await self._send_slack(message)
                elif channel == NOTIFICATION_EMAIL:
                    await self._send_email(message, level)
            except Exception as e:
                logger.error(f"Failed to send notification via {channel}: {e}")
    
    async def _send_console(self, message: str, level: str):
        """Send console notification"""
        if level == "error":
            logger.error(f"\n{message}")
        elif level == "warning":
            logger.warning(f"\n{message}")
        else:
            logger.info(f"\n{message}")
    
    async def _send_slack(self, message: str):
        """Send Slack notification"""
        if not settings.SLACK_WEBHOOK_URL:
            return
        
        # TODO: Implement Slack webhook
        logger.debug(f"Slack notification: {message}")
    
    async def _send_email(self, message: str, level: str):
        """Send email notification"""
        if not settings.EMAIL_ENABLED:
            return
        
        # TODO: Implement email notification
        logger.debug(f"Email notification: {message}")
