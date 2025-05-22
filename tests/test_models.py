"""
Tests for the models module
"""

import pytest
from oneworldsync.models import Content1Product, Content1ProductResults, Content1Hierarchy, Content1HierarchyResults


def test_content1_product_init():
    """Test Content1Product initialization"""
    data = {
        'gtin': '00000000000001',
        'informationProviderGLN': '1234567890123',
        'targetMarket': 'US',
        'lastModifiedDate': '2023-01-01T12:00:00Z',
        'item': {
            'brandName': 'Test Brand',
            'gpcCategory': '10000000'
        }
    }
    
    product = Content1Product(data)
    
    assert product.gtin == '00000000000001'
    assert product.information_provider_gln == '1234567890123'
    assert product.target_market == 'US'
    assert product.last_modified_date == '2023-01-01T12:00:00Z'
    assert product.brand_name == 'Test Brand'
    assert product.gpc_category == '10000000'


def test_content1_product_to_dict():
    """Test Content1Product to_dict method"""
    data = {
        'gtin': '00000000000001',
        'informationProviderGLN': '1234567890123',
        'targetMarket': 'US',
        'lastModifiedDate': '2023-01-01T12:00:00Z',
        'item': {
            'brandName': 'Test Brand',
            'gpcCategory': '10000000'
        }
    }
    
    product = Content1Product(data)
    product_dict = product.to_dict()
    
    assert product_dict['gtin'] == '00000000000001'
    assert product_dict['information_provider_gln'] == '1234567890123'
    assert product_dict['target_market'] == 'US'
    assert product_dict['last_modified_date'] == '2023-01-01T12:00:00Z'
    assert product_dict['brand_name'] == 'Test Brand'
    assert product_dict['gpc_category'] == '10000000'


def test_content1_product_results_init(mock_content1_response):
    """Test Content1ProductResults initialization"""
    results = Content1ProductResults(mock_content1_response)
    
    assert results.search_after == 'next_page_token'
    assert len(results.products) == 2
    assert isinstance(results.products[0], Content1Product)
    assert results.products[0].gtin == '00000000000001'
    assert results.products[1].gtin == '00000000000002'


def test_content1_product_results_iteration(mock_content1_response):
    """Test Content1ProductResults iteration"""
    results = Content1ProductResults(mock_content1_response)
    
    products = list(results)
    assert len(products) == 2
    assert products[0].gtin == '00000000000001'
    assert products[1].gtin == '00000000000002'


def test_content1_product_results_indexing(mock_content1_response):
    """Test Content1ProductResults indexing"""
    results = Content1ProductResults(mock_content1_response)
    
    assert results[0].gtin == '00000000000001'
    assert results[1].gtin == '00000000000002'


def test_content1_product_results_to_dict(mock_content1_response):
    """Test Content1ProductResults to_dict method"""
    results = Content1ProductResults(mock_content1_response)
    results_dict = results.to_dict()
    
    assert results_dict['metadata']['search_after'] == 'next_page_token'
    assert len(results_dict['products']) == 2
    assert results_dict['products'][0]['gtin'] == '00000000000001'
    assert results_dict['products'][1]['gtin'] == '00000000000002'


def test_content1_hierarchy_init(mock_content1_hierarchy_response):
    """Test Content1Hierarchy initialization"""
    hierarchy_data = mock_content1_hierarchy_response['hierarchies'][0]
    hierarchy = Content1Hierarchy(hierarchy_data)
    
    assert hierarchy.gtin == '00000000000001'
    assert hierarchy.information_provider_gln == '1234567890123'
    assert hierarchy.target_market == 'US'
    assert len(hierarchy.hierarchy) == 1
    assert hierarchy.hierarchy[0]['parentGtin'] == '00000000000001'
    assert hierarchy.hierarchy[0]['gtin'] == '00000000000002'
    assert hierarchy.hierarchy[0]['quantity'] == 2


def test_content1_hierarchy_to_dict(mock_content1_hierarchy_response):
    """Test Content1Hierarchy to_dict method"""
    hierarchy_data = mock_content1_hierarchy_response['hierarchies'][0]
    hierarchy = Content1Hierarchy(hierarchy_data)
    hierarchy_dict = hierarchy.to_dict()
    
    assert hierarchy_dict['gtin'] == '00000000000001'
    assert hierarchy_dict['information_provider_gln'] == '1234567890123'
    assert hierarchy_dict['target_market'] == 'US'
    assert len(hierarchy_dict['hierarchy']) == 1
    assert hierarchy_dict['hierarchy'][0]['parentGtin'] == '00000000000001'


def test_content1_hierarchy_results_init(mock_content1_hierarchy_response):
    """Test Content1HierarchyResults initialization"""
    results = Content1HierarchyResults(mock_content1_hierarchy_response)
    
    assert results.search_after == 'next_hierarchy_token'
    assert len(results.hierarchies) == 1
    assert isinstance(results.hierarchies[0], Content1Hierarchy)
    assert results.hierarchies[0].gtin == '00000000000001'


def test_content1_hierarchy_results_to_dict(mock_content1_hierarchy_response):
    """Test Content1HierarchyResults to_dict method"""
    results = Content1HierarchyResults(mock_content1_hierarchy_response)
    results_dict = results.to_dict()
    
    assert results_dict['metadata']['search_after'] == 'next_hierarchy_token'
    assert len(results_dict['hierarchies']) == 1
    assert results_dict['hierarchies'][0]['gtin'] == '00000000000001'