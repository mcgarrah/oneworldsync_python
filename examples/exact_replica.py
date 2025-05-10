#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exact replica of the medium_1ws_example.py script with minimal modifications.
This script is a direct copy of the working example with only the necessary changes to make it work.
"""

import hashlib
import hmac
import base64
import urllib
import datetime
import os
from dotenv import load_dotenv
import requests as r

# Load environment variables from .env file
load_dotenv()
APP_ID = os.getenv("ONEWORLDSYNC_APP_ID")
SECRET_KEY = os.getenv("ONEWORLDSYNC_SECRET_KEY")
API_URL = os.getenv("ONEWORLDSYNC_API_URL", "https://marketplace.preprod.api.1worldsync.com")

def main():
    """Main function implementing the exact replica of the working example"""
    
    # API Protocol, Domain, and Path
    PROTOCOL = 'https://'
    DOMAIN = API_URL.replace('https://', '') if API_URL.startswith('https://') else API_URL
    PATH = 'V2/products'
    
    # Query Parameters
    searchType = 'freeTextSearch'
    access_mdm = 'computer'
    query = "jelly"  # Using 'jelly' as the search term
    
    # Generate timestamp
    timestamp = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Optional Parameters
    geo_loc_access_latd = 9.91
    geo_loc_access_long = 51.51
    
    # String to hash - exactly as in the original example
    string_to_hash = f"/{PATH}?app_id={APP_ID}&searchType={searchType}&query={query}&access_mdm={access_mdm}&TIMESTAMP={timestamp}&geo_loc_access_latd={geo_loc_access_latd}&geo_loc_access_long={geo_loc_access_long}"
    print(f"String to hash: {string_to_hash}")
    
    # Hashing Custom String
    message = bytes(string_to_hash, 'utf-8')  # data bytes
    secret = bytes(SECRET_KEY, 'utf-8')  # key bytes
    hash = hmac.new(secret, message, hashlib.sha256)
    
    # Retrieving Hash Code
    hash_code = base64.b64encode(hash.digest())
    urlencoded_hash = urllib.parse.quote(hash_code).replace('/', '%2F')
    print(f"Generated hash code: {hash_code.decode('utf-8')}")
    
    # Constructing the request URL - exactly as in the original example
    requestURL = f"{PROTOCOL}{DOMAIN}/{PATH}?app_id={APP_ID}&searchType={searchType}&query={urllib.parse.quote(query)}&access_mdm={access_mdm}&TIMESTAMP={urllib.parse.quote(timestamp)}&geo_loc_access_latd={geo_loc_access_latd}&geo_loc_access_long={geo_loc_access_long}&hash_code={urlencoded_hash}"
    print(f"Request URL: {requestURL}")
    
    # Making the GET Request
    response = r.get(requestURL)
    
    # Check if the request was successful
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        print("Success!")
        # Process the response data
        data = response.json()
        print(f"Total results: {data.get('totalNumOfResults', '0')}")
        print(f"Number of results in this response: {len(data.get('results', []))}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    main()