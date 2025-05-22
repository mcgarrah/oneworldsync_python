#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced example script demonstrating how to use the 1WorldSync Content1 API client.
This example shows more complex queries and pagination handling.
"""

import os
import json
import datetime
from dotenv import load_dotenv
from oneworldsync import Content1Client, AuthenticationError, APIError

# Load environment variables from .env file
load_dotenv()
ONEWORLDSYNC_APP_ID = os.getenv("ONEWORLDSYNC_APP_ID")
ONEWORLDSYNC_SECRET_KEY = os.getenv("ONEWORLDSYNC_SECRET_KEY")
ONEWORLDSYNC_USER_GLN = os.getenv("ONEWORLDSYNC_USER_GLN")
ONEWORLDSYNC_CONTENT1_API_URL = os.getenv("ONEWORLDSYNC_CONTENT1_API_URL", "https://content1-api.1worldsync.com")

def main():
    """Main function demonstrating advanced Content1 API client usage"""
    
    # Initialize client
    client = Content1Client(
        app_id=ONEWORLDSYNC_APP_ID,
        secret_key=ONEWORLDSYNC_SECRET_KEY,
        gln=ONEWORLDSYNC_USER_GLN,
        api_url=ONEWORLDSYNC_CONTENT1_API_URL
    )
    
    try:
        # Example 1: Create a date range for the last 30 days
        today = datetime.datetime.now()
        thirty_days_ago = today - datetime.timedelta(days=30)
        
        date_criteria = {
            "lastModifiedDate": {
                "from": {
                    "date": thirty_days_ago.strftime("%Y-%m-%d"),
                    "op": "GTE"
                },
                "to": {
                    "date": today.strftime("%Y-%m-%d"),
                    "op": "LTE"
                }
            }
        }
        
        # Count products modified in the last 30 days
        print("Counting products modified in the last 30 days...")
        count = client.count_products(date_criteria)
        print(f"Products modified in the last 30 days: {count}")
        
        # Example 2: Fetch products with specific fields and sorting
        print("\nFetching products with specific fields and sorting...")
        
        fetch_criteria = {
            # Target market (e.g., US)
            "targetMarket": "US",
            
            # Date range (last 30 days)
            "lastModifiedDate": date_criteria["lastModifiedDate"],
            
            # Fields to include in the response
            "fields": {
                "include": [
                    "gtin",
                    "informationProviderGLN",
                    "targetMarket",
                    "lastModifiedDate",
                    "brandName",
                    "gpcCategory"
                ]
            },
            
            # Sort by last modified date (descending) and GTIN (ascending)
            "sortFields": [
                {
                    "field": "lastModifiedDate",
                    "desc": True
                },
                {
                    "field": "gtin",
                    "desc": False
                }
            ]
        }
        
        # Fetch first page with 10 products
        products = client.fetch_products(fetch_criteria, page_size=10)
        
        # Check if we have items in the response
        if "items" in products and products["items"]:
            print(f"Found {len(products['items'])} products on first page")
            
            # Save the first page to a file
            with open("content1_products_page1.json", "w") as f:
                json.dump(products, f, indent=2)
            
            print("First page saved to content1_products_page1.json")
            
            # Example 3: Pagination - fetch next page if available
            if "searchAfter" in products:
                print("\nFetching next page...")
                
                # Create criteria for next page
                next_page_criteria = fetch_criteria.copy()
                next_page_criteria["searchAfter"] = products["searchAfter"]
                
                # Fetch next page
                next_page = client.fetch_products(next_page_criteria, page_size=10)
                
                if "items" in next_page and next_page["items"]:
                    print(f"Found {len(next_page['items'])} products on second page")
                    
                    # Save the second page to a file
                    with open("content1_products_page2.json", "w") as f:
                        json.dump(next_page, f, indent=2)
                    
                    print("Second page saved to content1_products_page2.json")
                else:
                    print("No products found on second page")
            else:
                print("No more pages available")
        else:
            print("No products found matching the criteria")
        
        # Example 4: Fetch product hierarchies
        print("\nFetching product hierarchies...")
        
        hierarchy_criteria = {
            "targetMarket": "US",
            "lastModifiedDate": date_criteria["lastModifiedDate"],
            "sortFields": [
                {
                    "field": "lastModifiedDate",
                    "desc": True
                }
            ]
        }
        
        hierarchies = client.fetch_hierarchies(hierarchy_criteria, page_size=5)
        
        if "hierarchies" in hierarchies and hierarchies["hierarchies"]:
            print(f"Found {len(hierarchies['hierarchies'])} product hierarchies")
            
            # Save hierarchies to a file
            with open("content1_hierarchies.json", "w") as f:
                json.dump(hierarchies, f, indent=2)
            
            print("Hierarchies saved to content1_hierarchies.json")
            
            # Print information about the first hierarchy
            first_hierarchy = hierarchies["hierarchies"][0]
            print("\nFirst hierarchy details:")
            print(f"  GTIN: {first_hierarchy.get('gtin', 'N/A')}")
            print(f"  Information Provider GLN: {first_hierarchy.get('informationProviderGLN', 'N/A')}")
            print(f"  Target Market: {first_hierarchy.get('targetMarket', 'N/A')}")
            
            # Print hierarchy structure if available
            if "hierarchy" in first_hierarchy and first_hierarchy["hierarchy"]:
                print("  Hierarchy structure:")
                for level in first_hierarchy["hierarchy"]:
                    parent_gtin = level.get("parentGtin", "N/A")
                    gtin = level.get("gtin", "N/A")
                    quantity = level.get("quantity", "N/A")
                    print(f"    Parent GTIN: {parent_gtin}, GTIN: {gtin}, Quantity: {quantity}")
                    
                    # Print children if available
                    if "children" in level and level["children"]:
                        print(f"    Children: {len(level['children'])}")
        else:
            print("No hierarchies found matching the criteria")
        
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