#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct example script for the 1WorldSync API.
This script directly implements the authentication and request logic without using the client library.
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
    """Main function implementing direct API access"""
    
    # API parameters
    protocol = 'https://'
    domain = API_URL.replace('https://', '') if API_URL.startswith('https://') else API_URL
    path = 'V2/products'
    
    # Query parameters
    search_type = 'freeTextSearch'
    query = 'jelly'  # Using 'jelly' as the search term
    access_mdm = 'computer'
    timestamp = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Optional parameters
    geo_loc_access_latd = 9.91
    geo_loc_access_long = 51.51
    
    # Construct the string to hash
    string_to_hash = f"/{path}?app_id={APP_ID}&searchType={search_type}&query={query}&access_mdm={access_mdm}&TIMESTAMP={timestamp}&geo_loc_access_latd={geo_loc_access_latd}&geo_loc_access_long={geo_loc_access_long}"
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
    url = f"{protocol}{domain}/{path}?app_id={APP_ID}&searchType={search_type}&query={urllib.parse.quote(query)}&access_mdm={access_mdm}&TIMESTAMP={urllib.parse.quote(timestamp)}&geo_loc_access_latd={geo_loc_access_latd}&geo_loc_access_long={geo_loc_access_long}&hash_code={urlencoded_hash}"
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