"""
Tests for the exceptions module
"""

import pytest
from oneworldsync.exceptions import OneWorldSyncError, AuthenticationError, APIError


def test_oneworldsync_error():
    """Test OneWorldSyncError"""
    error = OneWorldSyncError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)


def test_authentication_error():
    """Test AuthenticationError"""
    error = AuthenticationError("Authentication failed")
    assert str(error) == "Authentication failed"
    assert isinstance(error, OneWorldSyncError)


def test_api_error():
    """Test APIError"""
    error = APIError(400, "Bad request")
    assert str(error) == "API Error 400: Bad request"
    assert error.status_code == 400
    assert error.response is None
    assert isinstance(error, OneWorldSyncError)


def test_api_error_with_response():
    """Test APIError with response object"""
    mock_response = {"error": "Invalid parameter"}
    error = APIError(400, "Bad request", mock_response)
    assert str(error) == "API Error 400: Bad request"
    assert error.status_code == 400
    assert error.response == mock_response