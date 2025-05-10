#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for advanced search functionality in the 1WorldSync API.
This script tries different field names and query formats to find what works.
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

def make_direct_request(query, access_mdm='computer'):
    """Make a direct request to the 1WorldSync API without using the client library"""
    
    # API parameters
    protocol = 'https://'
    domain = API_URL.replace('https://', '') if API_URL.startswith('https://') else API_URL
    path = 'V2/products'
    search_type = 'advancedSearch'
    
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

def test_advanced_search():
    """Test different field names and formats for advanced search"""
    
    # UPC to search for
    upc = "00007252147019"
    
    # Test different field names and formats
    test_queries = [
        # Standard field names with different formats
        f"gtin:{upc}",
        f"itemId:{upc}",
        f"upc:{upc}",
        f"ean:{upc}",
        f"primaryId:{upc}",
        
        # With quotes
        f"gtin:\"{upc}\"",
        f"itemId:\"{upc}\"",
        
        # JSON-like format
        f"\"gtin\":\"{upc}\"",
        f"\"itemId\":\"{upc}\"",
        
        # Nested paths
        f"item.itemIdentificationInformation.itemIdentifier.itemId:{upc}",
        f"itemIdentificationInformation.itemIdentifier.itemId:{upc}",
        
        # With wildcards
        f"gtin:*{upc}*",
        f"itemId:*{upc}*",
        
        # Different cases
        f"GTIN:{upc}",
        f"ItemId:{upc}"
    ]
    
    print("Testing different field names and formats for advanced search...\n")
    
    for query in test_queries:
        print(f"\nTesting query: {query}")
        
        response = make_direct_request(query)
        
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Response code: {data.get('responseCode')}")
            print(f"Response message: {data.get('responseMessage')}")
            print(f"Total results: {data.get('totalNumOfResults', 0)}")
            print(f"Number of results: {len(data.get('results', []))}")
            
            # If we found results, print the first one
            if data.get('results'):
                print("\nFound a working query format!")
                print(f"Working query: {query}")
                
                # Print the first result's identifiers to verify
                item = data['results'][0]['item']
                if 'itemIdentificationInformation' in item and 'itemIdentifier' in item['itemIdentificationInformation']:
                    identifiers = item['itemIdentificationInformation']['itemIdentifier']
                    print("\nItem identifiers:")
                    for identifier in identifiers:
                        is_primary = identifier.get('isPrimary', 'false')
                        item_id = identifier.get('itemId', 'N/A')
                        id_type = identifier.get('itemIdType', {}).get('value', 'Unknown')
                        print(f"  {id_type}: {item_id}{' (Primary)' if is_primary == 'true' else ''}")
                
                return query
        else:
            print(f"Error: {response.text}")
    
    print("\nNo working query format found.")
    return None

if __name__ == "__main__":
    working_query = test_advanced_search()
    
    if working_query:
        print(f"\n\nSUCCESS! Use this query format in your code: {working_query}")
    else:
        print("\n\nFAILED: Could not find a working query format for advanced search.")