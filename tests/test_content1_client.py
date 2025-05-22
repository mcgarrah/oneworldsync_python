"""
Tests for the Content1 client module
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from oneworldsync.content1_client import Content1Client
from oneworldsync.exceptions import AuthenticationError, APIError


def test_content1_client_init_with_params(mock_content1_credentials):
    """Test Content1Client initialization with parameters"""
    client = Content1Client(
        app_id=mock_content1_credentials['app_id'],
        secret_key=mock_content1_credentials['secret_key'],
        gln=mock_content1_credentials['gln'],
        api_url=mock_content1_credentials['api_url']
    )
    
    assert client.app_id == mock_content1_credentials['app_id']
    assert client.secret_key == mock_content1_credentials['secret_key']
    assert client.gln == mock_content1_credentials['gln']
    assert client.api_url == mock_content1_credentials['api_url']


def test_content1_client_init_with_env(mock_content1_env_credentials):
    """Test Content1Client initialization with environment variables"""
    client = Content1Client()
    
    assert client.app_id == 'env_app_id'
    assert client.secret_key == 'env_secret_key'
    assert client.gln == 'env_gln'
    assert client.api_url == 'https://env.content1-api.1worldsync.com'


def test_content1_client_init_missing_credentials():
    """Test Content1Client initialization with missing credentials"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            Content1Client()


def test_content1_make_request_success():
    """Test successful Content1 API request"""
    client = Content1Client('test_app_id', 'test_secret_key')
    
    # Mock the auth.generate_auth_headers method
    with patch.object(client.auth, 'generate_auth_headers', return_value={'appId': 'test_app_id', 'hashCode': 'test_hash'}):
        # Mock the requests.request method
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'count': 10}
        
        with patch('requests.request', return_value=mock_response):
            response = client._make_request('GET', '/V1/product/count')
            
            assert response == {'count': 10}


def test_content1_make_request_auth_error():
    """Test Content1 API request with authentication error"""
    client = Content1Client('test_app_id', 'test_secret_key')
    
    # Mock the auth.generate_auth_headers method
    with patch.object(client.auth, 'generate_auth_headers', return_value={'appId': 'test_app_id', 'hashCode': 'test_hash'}):
        # Mock the requests.request method
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = 'Authentication failed'
        
        with patch('requests.request', return_value=mock_response):
            with pytest.raises(AuthenticationError):
                client._make_request('GET', '/V1/product/count')


def test_content1_make_request_api_error():
    """Test Content1 API request with API error"""
    client = Content1Client('test_app_id', 'test_secret_key')
    
    # Mock the auth.generate_auth_headers method
    with patch.object(client.auth, 'generate_auth_headers', return_value={'appId': 'test_app_id', 'hashCode': 'test_hash'}):
        # Mock the requests.request method
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = 'Bad request'
        
        with patch('requests.request', return_value=mock_response):
            with pytest.raises(APIError) as excinfo:
                client._make_request('GET', '/V1/product/count')
            
            assert excinfo.value.status_code == 400


def test_content1_count_products():
    """Test count_products method"""
    client = Content1Client('test_app_id', 'test_secret_key')
    
    # Mock the _make_request method
    with patch.object(client, '_make_request', return_value={'count': 42}):
        count = client.count_products()
        
        assert count == 42


def test_content1_fetch_products(mock_content1_response):
    """Test fetch_products method"""
    client = Content1Client('test_app_id', 'test_secret_key')
    
    # Mock the _make_request method
    with patch.object(client, '_make_request', return_value=mock_content1_response):
        results = client.fetch_products()
        
        assert 'items' in results
        assert len(results['items']) == 2
        assert results['searchAfter'] == 'next_page_token'


def test_content1_fetch_products_by_gtin(mock_content1_response):
    """Test fetch_products_by_gtin method"""
    client = Content1Client('test_app_id', 'test_secret_key')
    
    # Mock the fetch_products method
    with patch.object(client, 'fetch_products', return_value=mock_content1_response):
        results = client.fetch_products_by_gtin(['00000000000001'])
        
        assert 'items' in results
        assert len(results['items']) == 2


def test_content1_fetch_hierarchies(mock_content1_hierarchy_response):
    """Test fetch_hierarchies method"""
    client = Content1Client('test_app_id', 'test_secret_key')
    
    # Mock the _make_request method
    with patch.object(client, '_make_request', return_value=mock_content1_hierarchy_response):
        results = client.fetch_hierarchies()
        
        assert 'hierarchies' in results
        assert len(results['hierarchies']) == 1
        assert results['searchAfter'] == 'next_hierarchy_token'