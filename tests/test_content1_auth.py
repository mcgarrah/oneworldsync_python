"""
Tests for the Content1 auth module
"""

import pytest
import datetime
import re
import base64
import hmac
import hashlib
from unittest.mock import patch, MagicMock
from oneworldsync.content1_auth import Content1HMACAuth


def test_content1_hmac_auth_init():
    """Test Content1HMACAuth initialization"""
    auth = Content1HMACAuth('test_app_id', 'test_secret_key', 'test_gln')
    assert auth.app_id == 'test_app_id'
    assert auth.secret_key == 'test_secret_key'
    assert auth.gln == 'test_gln'


def test_content1_generate_timestamp():
    """Test timestamp generation"""
    auth = Content1HMACAuth('test_app_id', 'test_secret_key')
    timestamp = auth.generate_timestamp()
    
    # Check format: YYYY-MM-DDThh:mm:ssZ
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
    assert re.match(pattern, timestamp) is not None


def test_content1_generate_hash():
    """Test hash generation"""
    auth = Content1HMACAuth('test_app_id', 'test_secret_key')
    test_uri = "/V1/product/count?timestamp=2023-01-01T12:00:00Z"
    hash_code = auth.generate_hash(test_uri)
    
    # Verify the hash manually
    expected_hash = base64.b64encode(
        hmac.new(
            bytes('test_secret_key', 'utf-8'),
            bytes(test_uri, 'utf-8'),
            hashlib.sha256
        ).digest()
    ).decode('utf-8')
    
    assert hash_code == expected_hash


def test_content1_generate_auth_headers():
    """Test generation of authentication headers"""
    auth = Content1HMACAuth('test_app_id', 'test_secret_key', 'test_gln')
    
    # Mock the generate_hash method
    with patch.object(auth, 'generate_hash', return_value='test_hash_code'):
        headers = auth.generate_auth_headers('/V1/product/count?timestamp=2023-01-01T12:00:00Z')
        
        assert headers['Content-Type'] == 'application/json'
        assert headers['accept'] == 'application/json'
        assert headers['appId'] == 'test_app_id'
        assert headers['hashCode'] == 'test_hash_code'
        assert headers['gln'] == 'test_gln'


def test_content1_generate_auth_headers_no_gln():
    """Test generation of authentication headers without GLN"""
    auth = Content1HMACAuth('test_app_id', 'test_secret_key')
    
    # Mock the generate_hash method
    with patch.object(auth, 'generate_hash', return_value='test_hash_code'):
        headers = auth.generate_auth_headers('/V1/product/count?timestamp=2023-01-01T12:00:00Z')
        
        assert headers['Content-Type'] == 'application/json'
        assert headers['accept'] == 'application/json'
        assert headers['appId'] == 'test_app_id'
        assert headers['hashCode'] == 'test_hash_code'
        assert 'gln' not in headers