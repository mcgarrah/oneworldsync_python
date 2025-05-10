#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug example script for the 1WorldSync API client.
This script replicates the exact parameters from a working example to help diagnose issues.
"""

import os
import hashlib
import hmac
import base64
import urllib.parse
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
APP_ID = os.getenv("ONEWORLDSYNC_APP_ID")
SECRET_KEY = os.getenv("ONEWORLDSYNC_SECRET_KEY")
API_URL = os.getenv("ONEWORLDSYNC_API_URL", "https://marketplace.preprod.api.1worldsync.com")

def main():
    """Main function to test the 1WorldSync API with exact parameters"""
    
    # API parameters
    protocol = 'https://'
    domain = API_URL.replace('https://', '') if API_URL.startswith('https://') else API_URL
    path = 'V2/products'
    
    # Query parameters - using the exact parameters from the working example
    search_type = 'freeTextSearch'
    query = 'jerry'
    access_mdm = 'computer'
    timestamp = '2025-04-11T03:07:31Z'  # Using the exact timestamp from the working example
    
    # Construct the string to hash exactly as in the working example
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
        # Print the first part of the response
        print(response.text[:500] + "...")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    main()