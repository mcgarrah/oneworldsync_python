"""
Exceptions for the 1WorldSync API client

This module defines custom exceptions used by the 1WorldSync API client.
"""


class OneWorldSyncError(Exception):
    """Base exception for all 1WorldSync API errors"""
    pass


class AuthenticationError(OneWorldSyncError):
    """Exception raised for authentication errors"""
    pass


class APIError(OneWorldSyncError):
    """Exception raised for API errors"""
    
    def __init__(self, status_code, message, response=None):
        """
        Initialize API error
        
        Args:
            status_code (int): HTTP status code
            message (str): Error message
            response (object, optional): Full API response
        """
        self.status_code = status_code
        self.response = response
        super().__init__(f"API Error {status_code}: {message}")