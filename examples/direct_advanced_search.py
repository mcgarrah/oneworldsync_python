#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct implementation of an advanced search for the 1WorldSync API.
This script bypasses the client library to test advanced search directly.
"""

import os
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

def main():
    """Main function implementing direct advanced search"""
    
    # API parameters
    protocol = 'https://'
    domain = API_URL.replace('https://', '') if API_URL.startswith('https://') else API_URL
    path = 'V2/products'
    
    # Query parameters
    search_type = 'advancedSearch'
    upc = '00007252147019'
    field = 'gtin'  # Try different field names: gtin, upc, itemId, etc.
    query = f"{field}:{upc}"
    access_mdm = 'computer'
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
    
    # Check the response
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        print("Success!")
        # Print the response
        data = response.json()
        print(f"Total results: {data.get('totalNumOfResults', '0')}")
        print(f"Number of results in this response: {len(data.get('results', []))}")
        
        # Print details of the first product if available
        results = data.get('results', [])
        if results:
            item = results[0].get('item', {})
            identifiers = item.get('itemIdentificationInformation', {}).get('itemIdentifier', [])
            for identifier in identifiers:
                id_type = identifier.get('itemIdType', {}).get('value', 'Unknown')
                id_value = identifier.get('itemId', 'N/A')
                is_primary = identifier.get('isPrimary') == 'true'
                print(f"  {id_type}: {id_value}{' (Primary)' if is_primary else ''}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    main()