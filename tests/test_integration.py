"""
Integration tests for the 1WorldSync client

These tests require valid API credentials and will make actual API calls.
They are disabled by default and can be enabled by setting the ONEWORLDSYNC_RUN_INTEGRATION_TESTS
environment variable to 'true'.
"""

import os
import pytest
from oneworldsync import OneWorldSyncClient, AuthenticationError, APIError


# Skip all tests in this module if integration tests are not enabled
pytestmark = pytest.mark.skipif(
    os.environ.get('ONEWORLDSYNC_RUN_INTEGRATION_TESTS') != 'true',
    reason="Integration tests are disabled. Set ONEWORLDSYNC_RUN_INTEGRATION_TESTS=true to enable."
)


@pytest.fixture
def client():
    """Create a client with credentials from environment variables"""
    try:
        return OneWorldSyncClient()
    except ValueError as e:
        pytest.skip(f"Missing credentials: {e}")


def test_free_text_search(client):
    """Test free text search with actual API"""
    try:
        results = client.free_text_search('milk')
        
        # Basic validation of results
        assert results.response_code == '0'
        assert results.response_message == 'Success'
        assert results.total_results >= 0
        
        # If there are results, check the first one
        if results.products:
            product = results.products[0]
            assert product.item_id is not None
            
    except (AuthenticationError, APIError) as e:
        pytest.fail(f"API error: {e}")


def test_advanced_search(client):
    """Test advanced search with actual API"""
    try:
        # This test assumes there's at least one product with this brand
        results = client.advanced_search('brandName', 'Test')
        
        # Basic validation of results
        assert results.response_code == '0'
        assert results.response_message == 'Success'
        
    except (AuthenticationError, APIError) as e:
        pytest.fail(f"API error: {e}")


def test_get_product(client):
    """Test getting a product with actual API"""
    try:
        # First, search for a product
        search_results = client.free_text_search('milk', limit=1)
        
        # If there are results, get the first product
        if search_results.products:
            product_id = search_results.products[0].item_id
            product_data = client.get_product(product_id)
            
            # Basic validation of product data
            assert product_data is not None
            
        else:
            pytest.skip("No products found to test get_product")
            
    except (AuthenticationError, APIError) as e:
        pytest.fail(f"API error: {e}")