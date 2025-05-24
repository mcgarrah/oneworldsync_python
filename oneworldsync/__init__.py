"""
1WorldSync Content1 API Python Client

This package provides a Python client for interacting with the 1WorldSync Content1 API.
It handles authentication, request signing, and provides methods for accessing
various endpoints of the 1WorldSync Content1 API.
"""

from .content1_client import Content1Client
from .content1_auth import Content1HMACAuth
from .exceptions import OneWorldSyncError, AuthenticationError, APIError

__version__ = '0.2.2'
