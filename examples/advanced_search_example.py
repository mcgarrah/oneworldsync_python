#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example script demonstrating how to use the 1WorldSync Python client for advanced searches.
This script tests different field names for advanced searches to find the correct one.
"""

import os
from dotenv import load_dotenv
from oneworldsync import OneWorldSyncClient, AuthenticationError, APIError

# Load environment variables from .env file
load_dotenv()
APP_ID = os.getenv("ONEWORLDSYNC_APP_ID")
SECRET_KEY = os.getenv("ONEWORLDSYNC_SECRET_KEY")
API_URL = os.getenv("ONEWORLDSYNC_API_URL")

def main():
    """Main function demonstrating advanced search with different field names"""
    
    # Initialize client
    client = OneWorldSyncClient(app_id=ONEWORLDSYNC_APP_ID, secret_key=ONEWORLDSYNC_SECRET_KEY, api_url=ONEWORLDSYNC_API_URL)
    
    # UPC/GTIN to search for
    upc = "00007252147019"
    
    # List of possible field names for UPC/GTIN searches
    field_names = [
        "gtin",
        "upc",
        "ean",
        "itemId",
        "primaryId",
        "itemPrimaryId",
        "gtinId",
        "productId"
    ]
    
    # Try each field name
    for field_name in field_names:
        try:
            print(f"\nTrying advanced search with field '{field_name}' for UPC '{upc}'...")
            results = client.advanced_search(field_name, upc)
            
            # If successful, print results
            print(f"SUCCESS! Found {len(results)} products using field '{field_name}'")
            
            # Print search results summary
            print(f"Response code: {results.response_code}")
            print(f"Response message: {results.response_message}")
            print(f"Total results: {results.total_results}")
            
            # Print details of each product
            for i, product in enumerate(results, 1):
                print(f"\nProduct {i}:")
                print(f"  ID: {product.item_id}")
                print(f"  Brand: {product.brand_name}")
                print(f"  Name: {product.product_name}")
            
        except APIError as e:
            print(f"FAILED with field '{field_name}': {e}")
        
        except Exception as e:
            print(f"Unexpected error with field '{field_name}': {e}")

if __name__ == "__main__":
    main()