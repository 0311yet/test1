from fastapi import HTTPException, status
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base API exception"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ValidationError(APIError):
    """Validation error"""
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

class NotFoundError(APIError):
    """Resource not found error"""
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)

class ExchangeError(APIError):
    """Exchange API error"""
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_502_BAD_GATEWAY)

class AuthenticationError(APIError):
    """Authentication error"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)

async def handle_exception(exc: Exception) -> None:
    """Handle uncaught exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred"
    )
