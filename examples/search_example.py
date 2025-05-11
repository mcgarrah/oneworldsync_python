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
ONEWORLDSYNC_APP_ID = os.getenv("ONEWORLDSYNC_APP_ID")
ONEWORLDSYNC_SECRET_KEY = os.getenv("ONEWORLDSYNC_SECRET_KEY")
ONEWORLDSYNC_API_URL = os.getenv("ONEWORLDSYNC_API_URL")

def main():
    """Main function demonstrating the 1WorldSync client usage"""
    
    # Initialize client
    client = OneWorldSyncClient(app_id=ONEWORLDSYNC_APP_ID, secret_key=ONEWORLDSYNC_SECRET_KEY, api_url=ONEWORLDSYNC_API_URL)
    
    try:
        # Perform a free text search
        print("Performing free text search for 'milk'...")
        results = client.free_text_search(
            "milk"
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
            
            # Print item Identification Information if available
            iteminfo = product.item['itemIdentificationInformation']['itemReferenceIdInformation']
            if iteminfo:
                # Print item Identification Information if available
                print(f"  itemReferenceId: {iteminfo['itemReferenceId']}")

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
        

        # Advanced search on Print product attributes if available

        # Advanced search example
        print("\n\nPerforming advanced search for UPC '16241419122223' (milk)...")
        
        # Try different field names for UPC searches
        upc = "16241419122223"  #milk search
        field_names = ["itemIdentifier"]

        for field in field_names:
            print(f"\nTrying field name: {field}")
            try:
                adv_results = client.advanced_search(field, upc)
                print(f"Success! Found {len(adv_results)} products")
                print(f"Response code: {adv_results}")
                # If successful, break out of the loop
                break
            except APIError as e:
                print(f"Failed with field '{field}': {e}")
                print(f"Status code: {e.status_code}")
        
    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except APIError as e:
        print(f"API error: {e}")
        print(f"Status code: {e.status_code}")

if __name__ == "__main__":
    main()