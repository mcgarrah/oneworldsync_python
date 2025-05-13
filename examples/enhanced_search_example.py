#!/usr/bin/env python3
"""
Enhanced Search Example

This example demonstrates the enhanced product data extraction functionality
of the OneWorldSync Python client.
"""

import os
import json
from dotenv import load_dotenv
from oneworldsync import OneWorldSyncClient

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
app_id = os.getenv("ONEWORLDSYNC_APP_ID")
secret_key = os.getenv("ONEWORLDSYNC_SECRET_KEY")

# Initialize the client
client = OneWorldSyncClient(app_id, secret_key)

def main():
    """Run the enhanced search example"""
    # Perform a search
    search_term = "milk"
    print(f"\nSearching for '{search_term}'...\n")
    
    try:
        # Search for products
        results = client.free_text_search(search_term, limit=5)
        
        # Display search metadata
        print(f"Found {results.total_results} products")
        print(f"Response code: {results.response_code}")
        print(f"Response message: {results.response_message}")
        print(f"Next cursor: {results.next_cursor}")
        print(f"Showing first {len(results)} results\n")
        
        # Display product information using the enhanced properties
        for i, product in enumerate(results):
            print(f"--- Product {i+1} ---")
            print(f"Item ID: {product.item_id}")
            print(f"GTIN: {product.gtin}")
            print(f"Brand: {product.brand_name}")
            print(f"Name: {product.product_name}")
            print(f"Description: {product.description}")
            print(f"Primary Image: {product.primary_image_url}")
            print(f"Dimensions: {product.formatted_dimensions}")
            print(f"GPC Code: {product.gpc_code}")
            print(f"Category: {product.category}")
            print(f"Country of Origin: {product.country_of_origin}")
            print(f"Ingredients: {product.ingredients[:100]}..." if product.ingredients and len(product.ingredients) > 100 else f"Ingredients: {product.ingredients}")
            
            # Display all images
            print(f"Images ({len(product.images)}):")
            for img in product.images[:3]:  # Show up to 3 images
                print(f"  - {img['url']} (Primary: {img['is_primary']})")
            
            if len(product.images) > 3:
                print(f"  - ... and {len(product.images) - 3} more")
            
            print()
        
        # Example of using to_dict() method
        if results:
            print("\n--- Converting first product to dictionary ---")
            product_dict = results[0].to_dict()
            print(json.dumps(product_dict, indent=2))
            
            print("\n--- Converting entire search results to dictionary ---")
            results_dict = results.to_dict()
            print(f"Metadata: {json.dumps(results_dict['metadata'], indent=2)}")
            print(f"Number of products in dictionary: {len(results_dict['products'])}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()