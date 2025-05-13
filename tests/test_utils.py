"""
Tests for the utils module
"""

import pytest
from datetime import datetime, timezone
from oneworldsync.utils import (
    format_timestamp, parse_timestamp, extract_nested_value,
    get_nested_dict_value, extract_product_data, format_dimensions
)


def test_format_timestamp():
    """Test format_timestamp function"""
    # Test with specific datetime
    dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    timestamp = format_timestamp(dt)
    assert timestamp == '2023-01-01T12:00:00Z'
    
    # Test without datetime (should use current time)
    timestamp = format_timestamp()
    # Just check format, not exact value
    assert len(timestamp) == 20
    assert timestamp[-1] == 'Z'
    assert 'T' in timestamp


def test_parse_timestamp():
    """Test parse_timestamp function"""
    dt = parse_timestamp('2023-01-01T12:00:00Z')
    assert dt.year == 2023
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 12
    assert dt.minute == 0
    assert dt.second == 0


def test_extract_nested_value():
    """Test extract_nested_value function"""
    data = {
        'level1': {
            'level2': {
                'level3': 'value'
            },
            'list': [
                {'item': 1},
                {'item': 2}
            ]
        }
    }
    
    # Test valid path
    assert extract_nested_value(data, ['level1', 'level2', 'level3']) == 'value'
    
    # Test path with list index
    assert extract_nested_value(data, ['level1', 'list', 0, 'item']) == 1
    assert extract_nested_value(data, ['level1', 'list', 1, 'item']) == 2
    
    # Test invalid path
    assert extract_nested_value(data, ['level1', 'invalid']) is None
    assert extract_nested_value(data, ['level1', 'level2', 'invalid']) is None
    
    # Test with default value
    assert extract_nested_value(data, ['level1', 'invalid'], 'default') == 'default'
    
    # Test with non-dict/list
    assert extract_nested_value('string', ['key']) is None
    
    # Test with empty path
    assert extract_nested_value(data, []) == data


def test_get_nested_dict_value():
    """Test get_nested_dict_value function"""
    data = {
        'level1': {
            'level2': {
                'level3': 'value'
            },
            'list': [
                {'item': 1},
                {'item': 2}
            ]
        }
    }
    
    # Test valid path
    assert get_nested_dict_value(data, 'level1.level2.level3') == 'value'
    
    # Test path with list index
    assert get_nested_dict_value(data, 'level1.list.0.item') == 1
    assert get_nested_dict_value(data, 'level1.list.1.item') == 2
    
    # Test invalid path
    assert get_nested_dict_value(data, 'level1.invalid') is None
    assert get_nested_dict_value(data, 'level1.level2.invalid') is None
    
    # Test with default value
    assert get_nested_dict_value(data, 'level1.invalid', 'default') == 'default'
    
    # Test with non-dict
    assert get_nested_dict_value('string', 'key') is None
    
    # Test with empty path
    assert get_nested_dict_value(data, '') == data


def test_format_dimensions():
    """Test format_dimensions function"""
    # Test with all dimensions
    dimensions = {
        'height': {'value': '10', 'unit': 'CM'},
        'width': {'value': '20', 'unit': 'CM'},
        'depth': {'value': '30', 'unit': 'CM'}
    }
    assert format_dimensions(dimensions) == 'Height: 10 CM, Width: 20 CM, Depth: 30 CM'
    
    # Test with some dimensions
    dimensions = {
        'height': {'value': '10', 'unit': 'CM'},
        'width': {'value': '', 'unit': 'CM'},
        'depth': {'value': '30', 'unit': 'CM'}
    }
    assert format_dimensions(dimensions) == 'Height: 10 CM, Depth: 30 CM'
    
    # Test with empty dimensions
    assert format_dimensions({}) == ''
    
    # Test with None
    assert format_dimensions(None) == ''


def test_extract_product_data():
    """Test extract_product_data function"""
    # Create a minimal product data structure
    product_data = {
        'item': {
            'itemIdentificationInformation': {
                'itemIdentifier': [
                    {
                        'itemId': '12345678901234',
                        'itemIdType': {'value': 'GTIN'},
                        'isPrimary': 'true'
                    }
                ],
                'itemReferenceIdInformation': {
                    'itemReferenceId': 'ref123'
                }
            },
            'tradeItemInformation': [
                {
                    'tradeItemDescriptionModule': {
                        'tradeItemDescriptionInformation': [
                            {
                                'brandNameInformation': {
                                    'brandName': 'Test Brand'
                                },
                                'regulatedProductName': [
                                    {
                                        'statement': {
                                            'values': [
                                                {'value': 'Test Product', 'language': 'en'}
                                            ]
                                        }
                                    }
                                ],
                                'additionalTradeItemDescription': {
                                    'values': [
                                        {'value': 'Test Description', 'language': 'en'}
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
    
    result = extract_product_data(product_data)
    
    # Check basic fields
    assert result['gtin'] == '12345678901234'
    assert result['brand_name'] == 'Test Brand'
    assert result['product_name'] == 'Test Product'
    assert result['description'] == 'Test Description'
    assert result['item_id'] == 'ref123'
    
    # Test with empty data
    empty_result = extract_product_data({})
    assert empty_result['gtin'] == ''
    assert empty_result['brand_name'] == ''
    assert empty_result['product_name'] == ''