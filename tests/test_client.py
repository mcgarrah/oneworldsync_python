"""
Tests for the client module
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from oneworldsync.client import OneWorldSyncClient
from oneworldsync.exceptions import AuthenticationError, APIError
from oneworldsync.models import SearchResults


def test_client_init_with_params(mock_credentials):
    """Test client initialization with parameters"""
    client = OneWorldSyncClient(
        app_id=mock_credentials['app_id'],
        secret_key=mock_credentials['secret_key'],
        api_url=mock_credentials['api_url']
    )
    
    assert client.app_id == mock_credentials['app_id']
    assert client.secret_key == mock_credentials['secret_key']
    assert client.domain == mock_credentials['api_url']


def test_client_init_with_env(mock_env_credentials):
    """Test client initialization with environment variables"""
    client = OneWorldSyncClient()
    
    assert client.app_id == 'env_app_id'
    assert client.secret_key == 'env_secret_key'
    assert client.domain == 'env.api.1worldsync.com'


def test_client_init_missing_credentials():
    """Test client initialization with missing credentials"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            OneWorldSyncClient()


def test_make_request_success():
    """Test successful API request"""
    client = OneWorldSyncClient('test_app_id', 'test_secret_key')
    
    # Mock the auth.get_auth_url method
    with patch.object(client.auth, 'get_auth_url', return_value='https://test.api.1worldsync.com/test'):
        # Mock the requests.request method
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'responseCode': '0', 'responseMessage': 'Success'}
        
        with patch('requests.request', return_value=mock_response):
            response = client._make_request('GET', 'test', {'param': 'value'})
            
            assert response == {'responseCode': '0', 'responseMessage': 'Success'}


def test_make_request_auth_error():
    """Test API request with authentication error"""
    client = OneWorldSyncClient('test_app_id', 'test_secret_key')
    
    # Mock the auth.get_auth_url method
    with patch.object(client.auth, 'get_auth_url', return_value='https://test.api.1worldsync.com/test'):
        # Mock the requests.request method
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = 'Authentication failed'
        
        with patch('requests.request', return_value=mock_response):
            with pytest.raises(AuthenticationError):
                client._make_request('GET', 'test', {'param': 'value'})


def test_make_request_api_error():
    """Test API request with API error"""
    client = OneWorldSyncClient('test_app_id', 'test_secret_key')
    
    # Mock the auth.get_auth_url method
    with patch.object(client.auth, 'get_auth_url', return_value='https://test.api.1worldsync.com/test'):
        # Mock the requests.request method
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = 'Bad request'
        
        with patch('requests.request', return_value=mock_response):
            with pytest.raises(APIError) as excinfo:
                client._make_request('GET', 'test', {'param': 'value'})
            
            assert excinfo.value.status_code == 400


def test_search_products(mock_response):
    """Test search_products method"""
    client = OneWorldSyncClient('test_app_id', 'test_secret_key')
    
    # Mock the _make_request method
    with patch.object(client, '_make_request', return_value=mock_response):
        results = client.search_products('milk')
        
        assert isinstance(results, SearchResults)
        assert len(results.products) == 2
        assert results.total_results == 2
        assert results.next_cursor == 'cursor123'


def test_free_text_search(mock_response):
    """Test free_text_search method"""
    client = OneWorldSyncClient('test_app_id', 'test_secret_key')
    
    # Mock the search_products method
    with patch.object(client, 'search_products', return_value=SearchResults(mock_response)):
        results = client.free_text_search('milk')
        
        assert isinstance(results, SearchResults)
        assert len(results.products) == 2


def test_advanced_search(mock_response):
    """Test advanced_search method"""
    client = OneWorldSyncClient('test_app_id', 'test_secret_key')
    
    # Mock the search_products method
    with patch.object(client, 'search_products', return_value=SearchResults(mock_response)):
        results = client.advanced_search('itemIdentifier', '12345')
        
        assert isinstance(results, SearchResults)
        assert len(results.products) == 2


def test_get_product(mock_response):
    """Test get_product method"""
    client = OneWorldSyncClient('test_app_id', 'test_secret_key')
    
    # Mock the _make_request method
    with patch.object(client, '_make_request', return_value=mock_response):
        product = client.get_product('item123')
        
        assert product == mock_response