#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to identify the correct field name for UPC/GTIN searches in the 1WorldSync API.
This script tries multiple field names and formats to find what works.
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

def make_direct_request(search_type, query, access_mdm='computer'):
    """Make a direct request to the 1WorldSync API without using the client library"""
    
    # API parameters
    protocol = 'https://'
    domain = API_URL.replace('https://', '') if API_URL.startswith('https://') else API_URL
    path = 'V2/products'
    
    # Query parameters
    timestamp = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Construct the string to hash
    string_to_hash = f"/{path}?app_id={APP_ID}&searchType={search_type}&query={query}&access_mdm={access_mdm}&TIMESTAMP={timestamp}"
    print(f"String to hash: {string_to_hash}")
    
    # Generate hash code
    message = bytes(string_to_hash, 'utf-8')
    secret = bytes(SECRET_KEY, 'utf-8')
    hash_obj = hmac.new(secret, message, hashlib.sha256)
    hash_code = base64.b64encode(hash_obj.digest()).decode('utf-8')
    print(f"Generated hash code: {hash_code}")
    
    # URL encode the hash code
    urlencoded_hash = urllib.parse.quote(hash_code).replace('/', '%2F')
    
    # Construct the full URL
    url = f"{protocol}{domain}/{path}?app_id={APP_ID}&searchType={search_type}&query={urllib.parse.quote(query)}&access_mdm={access_mdm}&TIMESTAMP={urllib.parse.quote(timestamp)}&hash_code={urlencoded_hash}"
    print(f"Request URL: {url}")
    
    # Make the request
    response = requests.get(url)
    
    # Return the response
    return response

def test_field_formats():
    """Test different field formats for UPC/GTIN searches"""
    
    # UPC to search for
    upc = "00007252147019"
    
    # Test different field formats
    field_formats = [
        # Standard field names
        "itemId:{0}",
        "gtin:{0}",
        "upc:{0}",
        "ean:{0}",
        
        # Nested field paths
        "item.itemIdentificationInformation.itemIdentifier.itemId:{0}",
        "itemIdentificationInformation.itemIdentifier.itemId:{0}",
        
        # With quotes
        "itemId:\"{0}\"",
        "gtin:\"{0}\"",
        
        # With wildcards
        "itemId:*{0}*",
        "gtin:*{0}*",
        
        # Different cases
        "ITEMID:{0}",
        "ItemId:{0}"
    ]
    
    print("Testing different field formats for UPC/GTIN searches...\n")
    
    for format_str in field_formats:
        query = format_str.format(upc)
        print(f"\nTesting query: {query}")
        
        response = make_direct_request('advancedSearch', query)
        
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Response code: {data.get('responseCode')}")
            print(f"Response message: {data.get('responseMessage')}")
            print(f"Total results: {data.get('totalNumOfResults', 0)}")
            print(f"Number of results: {len(data.get('results', []))}")
            
            # If we found results, print the first one
            if data.get('results'):
                print("\nFound a working field format!")
                print(f"Working query format: {format_str}")
                return format_str
        else:
            print(f"Error: {response.text}")
    
    print("\nNo working field format found.")
    return None

if __name__ == "__main__":
    test_field_formats()