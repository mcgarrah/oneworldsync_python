"""
1WorldSync Content1 API Python Client

This package provides a Python client for interacting with the 1WorldSync Content1 API.
It handles authentication, request signing, and provides methods for accessing
various endpoints of the 1WorldSync Content1 API.
"""

from .content1_client import Content1Client
from .content1_auth import Content1HMACAuth
from .exceptions import OneWorldSyncError, AuthenticationError, APIError
from .criteria import ProductCriteria, DateRangeCriteria, SortField
from .models import Content1Product, Content1ProductResults, Content1Hierarchy, Content1HierarchyResults

__version__ = '0.3.1'

__all__ = [
    'Content1Client',
    'Content1HMACAuth',
    'OneWorldSyncError',
    'AuthenticationError',
    'APIError',
    'ProductCriteria',
    'DateRangeCriteria',
    'SortField',
    'Content1Product',
    'Content1ProductResults',
    'Content1Hierarchy',
    'Content1HierarchyResults'
]
