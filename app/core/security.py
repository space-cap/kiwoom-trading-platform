"""
Security and authentication utilities
"""

import json
import os
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta
from threading import Lock

from app.core.logging import logger


class TokenManager:
    """Manage OAuth tokens for Kiwoom API with file persistence"""
    
    TOKEN_FILE = Path("data/.token")
    TOKEN_FILE_LOCK = Lock()
    
    def __init__(self):
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
        self._load_token_from_file()
    
    def _ensure_data_dir(self) -> None:
        """Ensure data directory exists"""
        self.TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_token_from_file(self) -> None:
        """Load token from file if exists and valid"""
        if not self.TOKEN_FILE.exists():
            return
        
        try:
            with self.TOKEN_FILE_LOCK:
                with open(self.TOKEN_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                access_token = data.get('access_token')
                expires_at_str = data.get('expires_at')
                
                if not access_token or not expires_at_str:
                    logger.warning("Invalid token file format")
                    return
                
                # Parse expiration time
                expires_at = datetime.fromisoformat(expires_at_str)
                
                # Check if token is still valid (with 5min buffer)
                if datetime.now() < expires_at - timedelta(minutes=5):
                    self._access_token = access_token
                    self._token_expires_at = expires_at
                    logger.info(f"Loaded valid token from file (expires at {expires_at})")
                else:
                    logger.info("Token in file has expired")
                    self._delete_token_file()
        
        except json.JSONDecodeError:
            logger.error("Failed to parse token file (invalid JSON)")
            self._delete_token_file()
        except Exception as e:
            logger.error(f"Failed to load token from file: {e}")
            self._delete_token_file()
    
    def _save_token_to_file(self) -> None:
        """Save token to file"""
        if not self._access_token or not self._token_expires_at:
            return
        
        try:
            self._ensure_data_dir()
            
            data = {
                'access_token': self._access_token,
                'expires_at': self._token_expires_at.isoformat(),
                'created_at': datetime.now().isoformat(),
            }
            
            with self.TOKEN_FILE_LOCK:
                # Write to temporary file first
                temp_file = self.TOKEN_FILE.with_suffix('.tmp')
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                
                # Atomic rename
                temp_file.replace(self.TOKEN_FILE)
                
                # Set file permissions (readable only by owner)
                if os.name != 'nt':  # Unix-like systems
                    os.chmod(self.TOKEN_FILE, 0o600)
            
            logger.info(f"Token saved to file (expires at {self._token_expires_at})")
        
        except Exception as e:
            logger.error(f"Failed to save token to file: {e}")
    
    def _delete_token_file(self) -> None:
        """Delete token file"""
        try:
            if self.TOKEN_FILE.exists():
                with self.TOKEN_FILE_LOCK:
                    self.TOKEN_FILE.unlink()
                logger.debug("Token file deleted")
        except Exception as e:
            logger.error(f"Failed to delete token file: {e}")
    
    def set_token(self, access_token: str, expires_in: int) -> None:
        """
        Set access token and expiration time
        
        Args:
            access_token: OAuth access token
            expires_in: Token expiration time in seconds
        """
        self._access_token = access_token
        self._token_expires_at = datetime.now() + timedelta(seconds=expires_in)
        
        # Save to file
        self._save_token_to_file()
        
        logger.info(f"Token set (expires in {expires_in}s)")
    
    def get_token(self) -> Optional[str]:
        """
        Get current access token if valid
        
        Returns:
            Access token or None if invalid/expired
        """
        # Try to load from file if not in memory
        if not self._access_token:
            self._load_token_from_file()
        
        if self._access_token and self._token_expires_at:
            # Check validity with 5min buffer
            if datetime.now() < self._token_expires_at - timedelta(minutes=5):
                return self._access_token
            else:
                logger.info("Token expired, clearing...")
                self.clear_token()
        
        return None
    
    def is_token_valid(self) -> bool:
        """
        Check if current token is valid
        
        Returns:
            True if token exists and is valid
        """
        return self.get_token() is not None
    
    def clear_token(self) -> None:
        """Clear token data from memory and file"""
        self._access_token = None
        self._token_expires_at = None
        self._delete_token_file()
        logger.info("Token cleared")
    
    def get_token_info(self) -> dict:
        """
        Get token information
        
        Returns:
            Dictionary with token info
        """
        if not self._access_token or not self._token_expires_at:
            return {
                'has_token': False,
                'is_valid': False,
            }
        
        now = datetime.now()
        is_valid = now < self._token_expires_at - timedelta(minutes=5)
        remaining_seconds = int((self._token_expires_at - now).total_seconds())
        
        return {
            'has_token': True,
            'is_valid': is_valid,
            'expires_at': self._token_expires_at.isoformat(),
            'remaining_seconds': remaining_seconds if is_valid else 0,
            'token_preview': f"{self._access_token[:20]}..." if self._access_token else None,
        }


# Global token manager instance
token_manager = TokenManager()
