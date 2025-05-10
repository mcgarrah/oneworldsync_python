"""
Utility functions for the 1WorldSync API client
"""

import json
from datetime import datetime


def format_timestamp(dt=None):
    """
    Format a datetime object as a timestamp for the 1WorldSync API
    
    Args:
        dt (datetime, optional): Datetime object to format. Defaults to current UTC time.
        
    Returns:
        str: Formatted timestamp
    """
    if dt is None:
        dt = datetime.now(datetime.UTC)
    
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


def parse_timestamp(timestamp_str):
    """
    Parse a timestamp string from the 1WorldSync API
    
    Args:
        timestamp_str (str): Timestamp string in ISO 8601 format
        
    Returns:
        datetime: Parsed datetime object
    """
    return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')


def pretty_print_json(data):
    """
    Pretty print JSON data
    
    Args:
        data (dict): JSON data to print
    """
    print(json.dumps(data, indent=2))


def extract_nested_value(data, path, default=None):
    """
    Extract a value from a nested dictionary using a path
    
    Args:
        data (dict): Dictionary to extract from
        path (list): List of keys to traverse
        default: Value to return if path doesn't exist
        
    Returns:
        The value at the path or the default value
    """
    current = data
    
    try:
        for key in path:
            if isinstance(current, dict):
                current = current.get(key)
            elif isinstance(current, list) and isinstance(key, int) and 0 <= key < len(current):
                current = current[key]
            else:
                return default
            
            if current is None:
                return default
        
        return current
    except (KeyError, IndexError, TypeError):
        return default