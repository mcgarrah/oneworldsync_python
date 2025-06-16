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
from oneworldsync import (
    Content1Client, 
    AuthenticationError, 
    APIError,
    ProductCriteria,
    DateRangeCriteria,
    SortField
)

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
        # Example 1: Create a date range for the last 30 days using the new DateRangeCriteria
        print("Counting products modified in the last 30 days...")
        
        # Create criteria using the builder pattern
        criteria = ProductCriteria().with_last_modified_date(DateRangeCriteria.last_30_days())
        
        # Count products modified in the last 30 days
        count = client.count_products(criteria)
        print(f"Products modified in the last 30 days: {count}")
        
        # Example 2: Fetch products with specific fields and sorting using the builder pattern
        print("\nFetching products with specific fields and sorting...")
        
        # Create criteria using the builder pattern
        fetch_criteria = ProductCriteria() \
            .with_target_market("US") \
            .with_last_modified_date(DateRangeCriteria.last_30_days()) \
            .with_fields(
                include=[
                    "gtin",
                    "informationProviderGLN",
                    "targetMarket",
                    "lastModifiedDate",
                    "brandName",
                    "gpcCategory"
                ]
            ) \
            .with_sort([
                SortField.create("lastModifiedDate", descending=True),
                SortField.create("gtin", descending=False)
            ])
        
        # Fetch first page with 10 products
        products = client.fetch_products(fetch_criteria, page_size=10)
        
        # Check if we have items in the response
        print(f"Found {len(products)} products on first page")
            
            # Save the first page to a file
            with open("content1_products_page1.json", "w") as f:
                json.dump(products, f, indent=2)
            
            print("First page saved to content1_products_page1.json")
            
            # Example 3: Pagination - fetch next page if available
            if products.search_after:
                print("\nFetching next page...")
                
                # Fetch next page using fetch_next_page with original criteria
                next_page = client.fetch_next_page(products, page_size=10, original_criteria=fetch_criteria)
                
                print(f"Found {len(next_page)} products on second page")
                    
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
        
        # Example 4: Fetch product hierarchies using the builder pattern
        print("\nFetching product hierarchies...")
        
        hierarchy_criteria = ProductCriteria() \
            .with_target_market("US") \
            .with_last_modified_date(DateRangeCriteria.last_30_days()) \
            .with_sort([
                SortField.create("lastModifiedDate", descending=True)
            ])
        
        hierarchies = client.fetch_hierarchies(hierarchy_criteria, page_size=5)
        
        print(f"Found {len(hierarchies)} product hierarchies")
            
            # Save hierarchies to a file
            with open("content1_hierarchies.json", "w") as f:
                json.dump(hierarchies, f, indent=2)
            
            print("Hierarchies saved to content1_hierarchies.json")
            
            # Print information about the first hierarchy
            first_hierarchy = hierarchies[0]
            print("\nFirst hierarchy details:")
            print(f"  GTIN: {first_hierarchy.gtin}")
            print(f"  Information Provider GLN: {first_hierarchy.information_provider_gln}")
            print(f"  Target Market: {first_hierarchy.target_market}")
            
            # Print hierarchy structure if available
            if first_hierarchy.hierarchy:
                print("  Hierarchy structure:")
                for level in first_hierarchy.hierarchy:
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
