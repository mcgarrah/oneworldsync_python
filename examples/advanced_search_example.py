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
ONEWORLDSYNC_APP_ID = os.getenv("ONEWORLDSYNC_APP_ID")
ONEWORLDSYNC_SECRET_KEY = os.getenv("ONEWORLDSYNC_SECRET_KEY")
ONEWORLDSYNC_API_URL = os.getenv("ONEWORLDSYNC_API_URL")

def main():
    """Main function demonstrating advanced search with different field names"""
    
    # Initialize client
    client = OneWorldSyncClient(app_id=ONEWORLDSYNC_APP_ID, secret_key=ONEWORLDSYNC_SECRET_KEY, api_url=ONEWORLDSYNC_API_URL)
    
    try:
        # Perform a free text search
        print("Performing free text search for 'milk'...")
        results = client.free_text_search(
            "milk"
        )

        # List to store itemReferenceId
        itemRefIdList = []
        
        # Print search results summary
        print(f"Response code: {results.response_code}")
        print(f"Response message: {results.response_message}")
        print(f"Total results: {results.total_results}")
        print(f"Results in this page: {len(results)}")
        
        # Print details of each product
        for i, product in enumerate(results, 1):
            print(f"\nProduct {i}:")
            print(f"  ID: {product.item_id}")
            print(f"  Brand: {product.brand_name}")
            print(f"  Name: {product.product_name}")
            
            # Print description if available
            if product.description:
                # Truncate long descriptions
                desc = product.description
                if len(desc) > 100:
                    desc = desc[:97] + "..."
                print(f"  Description: {desc}")
            
            # Print item Identification Information if available
            iteminfo = product.item['itemIdentificationInformation']['itemReferenceIdInformation']
            if iteminfo:
                # Print item Identification Information if available
                print(f"  itemReferenceId: {iteminfo['itemReferenceId']}")
                itemRefIdList.append(iteminfo['itemReferenceId'])

    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except APIError as e:
        print(f"API error: {e}")
        print(f"Status code: {e.status_code}")

        
    # UPC/GTIN to search for
    upc = "16241419122223"
    
    # List of possible field names for UPC/GTIN searches
    field_names = [
        "itemIdentifier"
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