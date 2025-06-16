#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example script demonstrating how to use date range filtering with the 1WorldSync Content1 API client.
"""

import os
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
    """Main function demonstrating date range filtering with the Content1 API client"""
    
    # Initialize client
    client = Content1Client(
        app_id=ONEWORLDSYNC_APP_ID,
        secret_key=ONEWORLDSYNC_SECRET_KEY,
        gln=ONEWORLDSYNC_USER_GLN,
        api_url=ONEWORLDSYNC_CONTENT1_API_URL
    )
    
    try:
        # Example 1: Get products from the last 30 days for US market
        print("Fetching US products from the last 30 days...")
        products = client.fetch_products_last_30_days(target_market="US", page_size=10)
        print(f"Found {len(products)} products")
        
        # Display the first few products
        for i, product in enumerate(products):
            if i >= 5:
                break
            print(f"  {i+1}. {product.brand_name} - {product.gtin} - {product.last_modified_date}")
        
        # Example 2: Get products from a specific date range
        print("\nFetching products from Jan 1-31, 2023...")
        products = client.fetch_products_by_date_range(
            from_date="2023-01-01",
            to_date="2023-01-31",
            target_market="US",
            page_size=10
        )
        print(f"Found {len(products)} products")
        
        # Example 3: Count products by date range and brand
        print("\nCounting products by date range and brand...")
        criteria = ProductCriteria() \
            .with_target_market("US") \
            .with_last_modified_date(DateRangeCriteria.last_30_days()) \
            .with_brand_name("Brand Name")
        
        count = client.count_products(criteria)
        print(f"Found {count} products matching the criteria")
        
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