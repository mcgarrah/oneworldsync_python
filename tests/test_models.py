"""
Tests for the models module
"""

import pytest
from oneworldsync.models import Product, SearchResults


def test_product_init(mock_response):
    """Test Product initialization"""
    product_data = mock_response['results'][0]
    product = Product(product_data)
    
    assert product.data == product_data
    assert product.item == product_data['item']


def test_product_item_id(mock_response):
    """Test Product.item_id property"""
    product = Product(mock_response['results'][0])
    assert product.item_id == 'item123'


def test_product_brand_name(mock_response):
    """Test Product.brand_name property"""
    product = Product(mock_response['results'][0])
    assert product.brand_name == 'Test Brand'


def test_product_product_name(mock_response):
    """Test Product.product_name property"""
    product = Product(mock_response['results'][0])
    assert product.product_name == 'Test Product'


def test_product_description(mock_response):
    """Test Product.description property"""
    product = Product(mock_response['results'][0])
    assert product.description == 'Test Description'


def test_product_images(mock_response):
    """Test Product.images property"""
    product = Product(mock_response['results'][0])
    images = product.images
    
    assert len(images) == 1
    assert images[0]['url'] == 'https://example.com/image.jpg'
    assert images[0]['is_primary'] is True


def test_product_dimensions(mock_response):
    """Test Product.dimensions property"""
    product = Product(mock_response['results'][0])
    dimensions = product.dimensions
    
    assert dimensions['height']['value'] == '10'
    assert dimensions['height']['unit'] == 'CM'
    assert dimensions['width']['value'] == '20'
    assert dimensions['width']['unit'] == 'CM'
    assert dimensions['depth']['value'] == '30'
    assert dimensions['depth']['unit'] == 'CM'


def test_product_str(mock_response):
    """Test Product.__str__ method"""
    product = Product(mock_response['results'][0])
    assert str(product) == 'Test Brand - Test Product (item123)'


def test_product_missing_data():
    """Test Product with missing data"""
    product = Product({'item': {}})
    
    assert product.item_id is None
    assert product.brand_name is None
    assert product.product_name is None
    assert product.description is None
    assert product.images == []
    assert product.dimensions == {}


def test_search_results_init(mock_response):
    """Test SearchResults initialization"""
    results = SearchResults(mock_response)
    
    assert results.data == mock_response
    assert results.response_code == '0'
    assert results.response_message == 'Success'
    assert results.total_results == 2
    assert results.next_cursor == 'cursor123'
    assert len(results.products) == 2


def test_search_results_len(mock_response):
    """Test SearchResults.__len__ method"""
    results = SearchResults(mock_response)
    assert len(results) == 2


def test_search_results_iter(mock_response):
    """Test SearchResults.__iter__ method"""
    results = SearchResults(mock_response)
    products = list(results)
    
    assert len(products) == 2
    assert products[0].item_id == 'item123'
    assert products[1].item_id == 'item456'


def test_search_results_getitem(mock_response):
    """Test SearchResults.__getitem__ method"""
    results = SearchResults(mock_response)
    
    assert results[0].item_id == 'item123'
    assert results[1].item_id == 'item456'


def test_search_results_empty():
    """Test SearchResults with empty data"""
    results = SearchResults({})
    
    assert results.response_code is None
    assert results.response_message is None
    assert results.total_results == 0
    assert results.next_cursor is None
    assert len(results.products) == 0