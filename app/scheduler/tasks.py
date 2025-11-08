"""
Scheduler tasks
"""

from datetime import datetime
from typing import List

from app.core.logging import logger
from app.core.database import SessionLocal
from app.shared.utils.datetime import is_market_open
from app.modules.condition.service import ConditionService
from app.modules.notifications.service import NotificationService


async def check_conditions_task():
    """
    Periodic task to check all active conditions
    """
    logger.info("Starting condition check task...")
    
    # Check if market is open
    if not is_market_open():
        logger.info("Market is closed, skipping condition check")
        return
    
    db = SessionLocal()
    notification_service = NotificationService()
    
    try:
        condition_service = ConditionService(db)
        
        # Get all active conditions
        conditions = condition_service.get_all_conditions(active_only=True)
        
        if not conditions:
            logger.info("No active conditions to check")
            return
        
        logger.info(f"Checking {len(conditions)} conditions...")
        
        # Check each condition
        for condition in conditions:
            try:
                # Execute condition search
                # Note: You'll need to provide user_id from settings or database
                result = await condition_service.execute_condition_search(
                    user_id="YOUR_USER_ID",  # TODO: Get from settings
                    seq=condition.seq
                )
                
                # Send notifications for new entries
                if result.new_entry_count > 0:
                    logger.info(
                        f"Condition '{condition.name}': "
                        f"{result.new_entry_count} new entries"
                    )
                    
                    for stock in result.results:
                        if stock.is_new_entry:
                            await notification_service.send_new_entry_alert(
                                condition_name=condition.name,
                                stock_code=stock.stock_code,
                                stock_name=stock.stock_name,
                                current_price=stock.current_price,
                                change_rate=stock.change_rate
                            )
                
            except Exception as e:
                logger.error(f"Failed to check condition '{condition.name}': {e}")
                await notification_service.send_error_alert(
                    error_message=str(e),
                    context=f"Condition: {condition.name}"
                )
        
        logger.info("Condition check task completed")
        
    except Exception as e:
        logger.exception(f"Condition check task failed: {e}")
        await notification_service.send_error_alert(
            error_message="Condition check task failed",
            context=str(e)
        )
    
    finally:
        db.close()


async def token_refresh_task():
    """
    Periodic task to refresh authentication token
    """
    logger.info("Refreshing authentication token...")
    
    try:
        from app.modules.auth.service import AuthService
        
        auth_service = AuthService()
        token_response = await auth_service.refresh_token()
        
        logger.info(f"Token refreshed successfully (expires in {token_response.expires_in}s)")
        
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
