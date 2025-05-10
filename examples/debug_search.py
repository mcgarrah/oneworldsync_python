#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug script for 1WorldSync API search functionality.
This script makes direct API calls to troubleshoot search issues.
"""

import os
import json
import hashlib
import hmac
import base64
import urllib.parse
import datetime
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
APP_ID = os.getenv("ONEWORLDSYNC_APP_ID")
SECRET_KEY = os.getenv("ONEWORLDSYNC_SECRET_KEY")
API_URL = os.getenv("ONEWORLDSYNC_API_URL", "https://marketplace.preprod.api.1worldsync.com")

def make_direct_request(search_type, query=None, access_mdm='computer', debug=True):
    """Make a direct request to the 1WorldSync API without using the client library"""
    
    # API parameters
    protocol = 'https://'
    domain = API_URL.replace('https://', '') if API_URL.startswith('https://') else API_URL
    path = 'V2/products'
    
    # Query parameters
    timestamp = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Build query parameters
    params = {
        'app_id': APP_ID,
        'access_mdm': access_mdm,
        'TIMESTAMP': timestamp
    }
    
    # Add search type and query if provided
    if search_type:
        params['searchType'] = search_type
    if query:
        params['query'] = query
    
    # Build query string
    query_string = '&'.join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    
    # Construct the string to hash
    string_to_hash = f"/{path}?{query_string}"
    if debug:
        print(f"String to hash: {string_to_hash}")
    
    # Generate hash code
    message = bytes(string_to_hash, 'utf-8')
    secret = bytes(SECRET_KEY, 'utf-8')
    hash_obj = hmac.new(secret, message, hashlib.sha256)
    hash_code = base64.b64encode(hash_obj.digest()).decode('utf-8')
    if debug:
        print(f"Generated hash code: {hash_code}")
    
    # URL encode the hash code
    urlencoded_hash = urllib.parse.quote(hash_code).replace('/', '%2F')
    
    # Construct the full URL
    url = f"{protocol}{domain}/{path}?{query_string}&hash_code={urlencoded_hash}"
    if debug:
        print(f"Request URL: {url}")
    
    # Make the request
    response = requests.get(url)
    
    # Return the response
    return response

def test_free_text_search():
    """Test free text search functionality"""
    print("\n=== Testing Free Text Search ===")
    
    # Test with different parameter formats
    search_queries = [
        ("freeTextSearch", "jelly"),
        ("freeTextSearch", "chocolate"),
        ("freetextsearch", "jelly"),  # Try lowercase
        ("free_text_search", "jelly"),  # Try with underscores
        ("freetext", "jelly"),  # Try abbreviated
    ]
    
    for search_type, query in search_queries:
        print(f"\nTesting search_type='{search_type}', query='{query}'")
        
        response = make_direct_request(search_type, query)
        
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Response code: {data.get('responseCode')}")
            print(f"Response message: {data.get('responseMessage')}")
            print(f"Total results: {data.get('totalNumOfResults', 0)}")
            print(f"Number of results: {len(data.get('results', []))}")
            
            # If we found results, we've identified a working format
            if data.get('results'):
                print(f"Working search format: search_type='{search_type}', query='{query}'")
                return search_type, query
        else:
            print(f"Error: {response.text}")
    
    print("\nNo working free text search format found.")
    return None, None

def test_advanced_search():
    """Test advanced search functionality"""
    print("\n=== Testing Advanced Search ===")
    
    # UPC to search for
    upc = "00007252147019"
    
    # Test different field formats and search types
    search_configs = [
        ("advancedSearch", f"itemId:{upc}"),
        ("advancedSearch", f"gtin:{upc}"),
        ("advancedSearch", f"upc:{upc}"),
        ("advancedSearch", f"item.itemIdentificationInformation.itemIdentifier.itemId:{upc}"),
        ("advancedSearch", f"itemIdentifier.itemId:{upc}"),
        ("advancedSearch", f"\"itemId\":\"{upc}\""),
        ("advancedSearch", f"itemId=\"{upc}\""),
        ("advanced", f"itemId:{upc}"),  # Try abbreviated
        ("advanced_search", f"itemId:{upc}"),  # Try with underscores
    ]
    
    for search_type, query in search_configs:
        print(f"\nTesting search_type='{search_type}', query='{query}'")
        
        response = make_direct_request(search_type, query)
        
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Response code: {data.get('responseCode')}")
            print(f"Response message: {data.get('responseMessage')}")
            print(f"Total results: {data.get('totalNumOfResults', 0)}")
            print(f"Number of results: {len(data.get('results', []))}")
            
            # If we found results, we've identified a working format
            if data.get('results'):
                print(f"Working search format: search_type='{search_type}', query='{query}'")
                return search_type, query
        else:
            print(f"Error: {response.text}")
    
    print("\nNo working advanced search format found.")
    return None, None

def test_api_connection():
    """Test basic API connection without search parameters"""
    print("\n=== Testing API Connection ===")
    
    # Make a request without search parameters to test authentication
    response = make_direct_request(None, None)
    
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        print("API connection successful!")
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        except:
            print(f"Response: {response.text}")
    else:
        print(f"API connection failed: {response.text}")

if __name__ == "__main__":
    print("1WorldSync API Search Debug Tool")
    print(f"Using APP_ID: {APP_ID}")
    print(f"Using SECRET_KEY: {'*' * len(SECRET_KEY)}")
    print(f"Using API_URL: {API_URL}")
    
    # Test API connection
    test_api_connection()
    
    # Test free text search
    test_free_text_search()
    
    # Test advanced search
    test_advanced_search()