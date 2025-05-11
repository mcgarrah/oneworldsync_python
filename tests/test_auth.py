"""
Tests for the auth module
"""

import pytest
import datetime
import re
import base64
import hmac
import hashlib
from unittest.mock import patch, MagicMock
from oneworldsync.auth import HMACAuth


def test_hmac_auth_init():
    """Test HMACAuth initialization"""
    auth = HMACAuth('test_app_id', 'test_secret_key')
    assert auth.app_id == 'test_app_id'
    assert auth.secret_key == 'test_secret_key'


def test_generate_timestamp():
    """Test timestamp generation"""
    auth = HMACAuth('test_app_id', 'test_secret_key')
    timestamp = auth.generate_timestamp()
    
    # Check format: YYYY-MM-DDThh:mm:ssZ
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
    assert re.match(pattern, timestamp) is not None


def test_generate_hash():
    """Test hash generation"""
    auth = HMACAuth('test_app_id', 'test_secret_key')
    test_string = "test_string_to_hash"
    hash_code = auth.generate_hash(test_string)
    
    # Verify the hash manually
    expected_hash = base64.b64encode(
        hmac.new(
            bytes('test_secret_key', 'utf-8'),
            bytes(test_string, 'utf-8'),
            hashlib.sha256
        ).digest()
    ).decode('utf-8')
    
    assert hash_code == expected_hash


def test_prepare_auth_params():
    """Test preparation of authentication parameters"""
    auth = HMACAuth('test_app_id', 'test_secret_key')
    
    # Mock the timestamp and hash generation
    with patch.object(auth, 'generate_timestamp', return_value='2023-01-01T12:00:00Z'):
        with patch.object(auth, 'generate_hash', return_value='test_hash_code'):
            params = auth.prepare_auth_params('V2/products', {'query': 'milk'})
            
            assert params['app_id'] == 'test_app_id'
            assert params['TIMESTAMP'] == '2023-01-01T12:00:00Z'
            assert params['hash_code'] == 'test_hash_code'
            assert params['query'] == 'milk'


def test_get_auth_url():
    """Test generation of authenticated URL"""
    auth = HMACAuth('test_app_id', 'test_secret_key')
    
    # Mock the prepare_auth_params method
    with patch.object(auth, 'prepare_auth_params', return_value={
        'app_id': 'test_app_id',
        'query': 'milk',
        'searchType': 'freeTextSearch',
        'access_mdm': 'computer',
        'TIMESTAMP': '2023-01-01T12:00:00Z',
        'hash_code': 'test/hash+code'
    }):
        url = auth.get_auth_url('https://', 'test.api.1worldsync.com', 'V2/products', {'query': 'milk'})
        
        # Check that the URL contains all parameters in the correct order
        expected_url_start = 'https://test.api.1worldsync.com/V2/products?app_id=test_app_id'
        assert url.startswith(expected_url_start)
        
        # Check that parameters are included and URL-encoded
        assert '&searchType=freeTextSearch' in url
        assert '&query=milk' in url
        assert '&access_mdm=computer' in url
        assert '&TIMESTAMP=2023-01-01T12%3A00%3A00Z' in url
        assert '&hash_code=test%2Fhash%2Bcode' in url