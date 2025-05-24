#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example script demonstrating how to use the 1WorldSync Content1 API client.
"""

import os
import json
from dotenv import load_dotenv
from oneworldsync import Content1Client, AuthenticationError, APIError

# Load environment variables from .env file
load_dotenv()
ONEWORLDSYNC_APP_ID = os.getenv("ONEWORLDSYNC_APP_ID")
ONEWORLDSYNC_SECRET_KEY = os.getenv("ONEWORLDSYNC_SECRET_KEY")
ONEWORLDSYNC_USER_GLN = os.getenv("ONEWORLDSYNC_USER_GLN")
ONEWORLDSYNC_CONTENT1_API_URL = os.getenv("ONEWORLDSYNC_CONTENT1_API_URL", "https://content1-api.1worldsync.com")

def main():
    """Main function demonstrating the 1WorldSync Content1 API client usage"""
    
    # Initialize client
    client = Content1Client(
        app_id=ONEWORLDSYNC_APP_ID,
        secret_key=ONEWORLDSYNC_SECRET_KEY,
        gln=ONEWORLDSYNC_USER_GLN,
        api_url=ONEWORLDSYNC_CONTENT1_API_URL
    )
    
    try:
        # Example 1: Count products
        print("Counting products...")
        count = client.count_products()
        print(f"Total products available: {count}")
        
        # Example 2: Fetch products by GTIN
        print("\nFetching products by GTIN...")
        # gtins = ["00000000000000"]  # Replace with actual GTINs
        gtins = [   "04711202220726",
                    "00022592008578",
                    "10072714008563",
                    "00037600168526",
                    "90037600257308",
                    "00072838196194",
                    "90037600162626",
                    "00028400083140",
                    "00018000428434",
                    "40012919122610",
                    "20044000026886",
                    "00068274000027",
                    "00840158101811",
                    "00079100514472",
                    "00850064944259",
                    "10721582133876",
                    "00767707014937",
                    "00044000026882",
                    "10810172671109",
                    "00760034121330",
                    "00075720481279",
                    "90037600094774",
                    "00032601953515",
                    "00028400147408",
                    "00079100851744"
        ]
        products = client.fetch_products_by_gtin(gtins)
        
        # Save the raw product details to a file for inspection
        with open("content1_products.json", "w") as f:
            json.dump(products, f, indent=2)
        
        print(f"Products saved to content1_products.json")
        
        # Example 3: Fetch products with criteria
        print("\nFetching products with custom criteria...")
        criteria = {
            "targetMarket": "US",
            "lastModifiedDate": {
                "from": {
                    "date": "2023-01-01",
                    "op": "GTE"
                },
                "to": {
                    "date": "2023-12-31",
                    "op": "LTE"
                }
            },
            "fields": {
                "include": [
                    "gtin",
                    "informationProviderGLN",
                    "targetMarket",
                    "lastModifiedDate",
                    "brandName",
                    "gpcCategory"
                ]
            }
        }
        
        products = client.fetch_products(criteria, page_size=10)
        
        # Check if we have items in the response
        if "items" in products and products["items"]:
            print(f"Found {len(products['items'])} products")
            
            # Display information about the first product
            first_product = products["items"][0]
            print("\nFirst product details:")
            
            # Extract and print GTIN if available
            if "gtin" in first_product:
                print(f"  GTIN: {first_product['gtin']}")
            
            # Extract and print item details if available
            if "item" in first_product:
                item = first_product["item"]
                
                # Try to extract brand name
                try:
                    brand_name = item.get("brandName", "N/A")
                    print(f"  Brand: {brand_name}")
                except (KeyError, TypeError):
                    print("  Brand: N/A")
                
                # Try to extract GPC category
                try:
                    gpc_category = item.get("gpcCategory", "N/A")
                    print(f"  GPC Category: {gpc_category}")
                except (KeyError, TypeError):
                    print("  GPC Category: N/A")
            
            # Check if there are more pages
            if "searchAfter" in products:
                print("\nMore pages available. Use fetch_next_page to retrieve them.")
        else:
            print("No products found matching the criteria.")
        
    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except APIError as e:
        print(f"API error: {e}")
        if hasattr(e, 'status_code'):
            print(f"Status code: {e.status_code}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()