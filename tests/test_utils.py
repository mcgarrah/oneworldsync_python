"""
Tests for the utils module
"""

import pytest
from datetime import datetime, timezone
from oneworldsync.utils import format_timestamp, parse_timestamp, extract_nested_value


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