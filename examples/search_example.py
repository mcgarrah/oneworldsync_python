#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example script demonstrating how to use the 1WorldSync Python client for searching products.
"""

import os
from dotenv import load_dotenv
from oneworldsync import OneWorldSyncClient, AuthenticationError, APIError

# Load environment variables from .env file
load_dotenv()
APP_ID = os.getenv("APP_ID")
SECRET_KEY = os.getenv("SECRET_KEY")

def main():
    """Main function demonstrating the 1WorldSync client usage"""
    
    # Initialize client (using preprod environment)
    client = OneWorldSyncClient(APP_ID, SECRET_KEY, use_production=False)
    
    try:
        # Perform a free text search
        print("Performing free text search for 'jerry'...")
        results = client.free_text_search(
            "jerry",
            geo_location=(9.91, 51.51)  # Optional geo location
        )
        
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
            
            # Print dimensions if available
            dimensions = product.dimensions
            if dimensions and dimensions.get('height', {}).get('value'):
                print(f"  Dimensions: {dimensions['height']['value']} {dimensions['height']['unit']} x "
                      f"{dimensions['width']['value']} {dimensions['width']['unit']} x "
                      f"{dimensions['depth']['value']} {dimensions['depth']['unit']}")
            
            # Print image URLs if available
            images = product.images
            if images:
                print(f"  Images: {len(images)}")
                for j, image in enumerate(images[:3], 1):  # Show up to 3 images
                    print(f"    Image {j}: {image['url']} (Primary: {image['is_primary']})")
                if len(images) > 3:
                    print(f"    ... and {len(images) - 3} more images")
        
        # Advanced search example
        print("\n\nPerforming advanced search for UPC '00007252147019'...")
        adv_results = client.advanced_search("itemPrimaryId", "00007252147019")
        print(f"Found {len(adv_results)} products")
        
    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except APIError as e:
        print(f"API error: {e}")
        print(f"Status code: {e.status_code}")

if __name__ == "__main__":
    main()