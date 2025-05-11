"""
1WorldSync API Python Client

This package provides a Python client for interacting with the 1WorldSync API.
It handles authentication, request signing, and provides methods for accessing
various endpoints of the 1WorldSync API.
"""

from .client import OneWorldSyncClient
from .auth import HMACAuth
from .exceptions import OneWorldSyncError, AuthenticationError, APIError

__version__ = '0.1.2'
