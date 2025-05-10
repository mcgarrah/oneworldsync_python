#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example script demonstrating how to use the 1WorldSync Python client for fetching product details.
"""

import os
import json
from dotenv import load_dotenv
from oneworldsync import OneWorldSyncClient, AuthenticationError, APIError

# Load environment variables from .env file
load_dotenv()
ONEWORLDSYNC_APP_ID = os.getenv("ONEWORLDSYNC_APP_ID")
ONEWORLDSYNC_SECRET_KEY = os.getenv("ONEWORLDSYNC_SECRET_KEY")
ONEWORLDSYNC_API_URL = os.getenv("ONEWORLDSYNC_API_URL")

def main():
    """Main function demonstrating the 1WorldSync client usage for product fetching"""
    
    # Initialize client
    client = OneWorldSyncClient(app_id=ONEWORLDSYNC_APP_ID, secret_key=ONEWORLDSYNC_SECRET_KEY, api_url=ONEWORLDSYNC_API_URL)
    
    try:
        # First, search for a product to get its ID
        print("Searching for a product to get its ID...")
        results = client.free_text_search("apple", limit=1)
        
        if not results.products:
            print("No products found in search.")
            return
        
        # Get the first product's ID
        product = results.products[0]
        product_id = product.item_id
        
        if not product_id:
            print("Could not determine product ID from search results.")
            return
        
        print(f"Found product: {product.brand_name} - {product.product_name}")
        print(f"Product ID: {product_id}")
        
        # Now fetch the complete product details
        print(f"\nFetching complete details for product {product_id}...")
        product_details = client.get_product(product_id)
        
        # Save the raw product details to a file for inspection
        with open("product_details.json", "w") as f:
            json.dump(product_details, f, indent=2)
        
        print(f"Product details saved to product_details.json")
        
        # Extract and display some key information
        if 'item' in product_details:
            item = product_details['item']
            
            # Display basic information
            print("\nProduct Information:")
            
            # Brand and name
            try:
                info = item.get('tradeItemInformation', [])[0]
                desc_module = info.get('tradeItemDescriptionModule', {})
                desc_info = desc_module.get('tradeItemDescriptionInformation', [])[0]
                brand = desc_info.get('brandNameInformation', {}).get('brandName', 'N/A')
                
                reg_names = desc_info.get('regulatedProductName', [])
                name = "N/A"
                if reg_names:
                    name = reg_names[0].get('statement', {}).get('values', [])[0].get('value', 'N/A')
                
                print(f"  Brand: {brand}")
                print(f"  Name: {name}")
            except (IndexError, KeyError):
                print("  Could not extract brand/name information")
            
            # Identifiers
            try:
                id_info = item.get('itemIdentificationInformation', {})
                identifiers = id_info.get('itemIdentifier', [])
                
                print("\nIdentifiers:")
                for identifier in identifiers:
                    id_type = identifier.get('itemIdType', {}).get('value', 'Unknown')
                    id_value = identifier.get('itemId', 'N/A')
                    is_primary = identifier.get('isPrimary') == 'true'
                    print(f"  {id_type}: {id_value}{' (Primary)' if is_primary else ''}")
            except (IndexError, KeyError):
                print("  Could not extract identifier information")
            
            # Classification
            try:
                categories = item.get('productCategory', [])
                
                print("\nCategories:")
                for category in categories:
                    scheme = category.get('productCategoryScheme', {}).get('value', 'Unknown')
                    codes = category.get('productCategoryCodes', [])
                    
                    print(f"  Scheme: {scheme}")
                    for code in codes:
                        code_value = code.get('productCategoryCode', {}).get('value', 'N/A')
                        component = code.get('productCategoryComponent', {}).get('value', 'N/A')
                        print(f"    {component}: {code_value}")
            except (IndexError, KeyError):
                print("  Could not extract category information")
        
    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except APIError as e:
        print(f"API error: {e}")
        print(f"Status code: {e.status_code}")

if __name__ == "__main__":
    main()