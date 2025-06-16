"""
Examples of using the enhanced Content1Client for product searches

This module demonstrates how to use the enhanced Content1Client to search for products
using various criteria.
"""

import os
from oneworldsync import (
    Content1Client, 
    ProductCriteria, 
    DateRangeCriteria, 
    SortField
)

# Initialize client with credentials from environment variables
client = Content1Client()

def example_search_by_date_range():
    """Example of searching products by date range"""
    print("Fetching products modified in the last 30 days for US market:")
    results = client.fetch_products_last_30_days(target_market="US")
    
    print(f"Found {len(results)} products")
    for product in results:
        print(f"- {product}")

def example_search_with_criteria_builder():
    """Example of using the criteria builder for complex searches"""
    # Create criteria for products:
    # - In the US market
    # - Modified in the last 30 days
    # - From a specific brand
    # - Sorted by last modified date (newest first)
    criteria = ProductCriteria() \
        .with_target_market("US") \
        .with_last_modified_date(DateRangeCriteria.last_30_days()) \
        .with_brand_name("Brand Name") \
        .with_sort([SortField.create("lastModifiedDate", descending=True)])
    
    print("Searching with complex criteria:")
    results = client.fetch_products(criteria)
    
    print(f"Found {len(results)} products")
    for product in results:
        print(f"- {product}")

def example_count_products_by_gpc():
    """Example of counting products by GPC code"""
    # Count products with a specific GPC code
    criteria = ProductCriteria() \
        .with_gpc_code("10000248") \
        .with_target_market("US")
    
    count = client.count_products(criteria)
    print(f"Found {count} products with GPC code 10000248 in US market")

def example_pagination():
    """Example of paginating through results"""
    # First page
    criteria = ProductCriteria().with_target_market("US")
    page1 = client.fetch_products(criteria, page_size=10)
    
    print(f"Page 1: {len(page1)} products")
    
    # If there are more results, fetch the next page
    if page1.search_after:
        page2 = client.fetch_next_page(page1, page_size=10, original_criteria=criteria)
        print(f"Page 2: {len(page2)} products")

if __name__ == "__main__":
    # Uncomment the examples you want to run
    # example_search_by_date_range()
    # example_search_with_criteria_builder()
    # example_count_products_by_gpc()
    # example_pagination()
    
    # Or run a simple example
    print("Running a simple example to fetch products from the last 30 days:")
    
    try:
        results = client.fetch_products_last_30_days(target_market="US", page_size=5)
        print(f"Found {len(results)} products")
        
        for i, product in enumerate(results):
            print(f"{i+1}. {product.brand_name} - {product.gtin}")
            
    except Exception as e:
        print(f"Error: {e}")