#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to extract all records with target market 'US' and write them to JSON files
in batches, keeping each file under 25MB (approximately 1000 records per file).
"""

import os
import json
import sys
from datetime import datetime
from dotenv import load_dotenv
from oneworldsync import Content1Client, AuthenticationError, APIError

# Load environment variables from .env file
load_dotenv()
ONEWORLDSYNC_APP_ID = os.getenv("ONEWORLDSYNC_APP_ID")
ONEWORLDSYNC_SECRET_KEY = os.getenv("ONEWORLDSYNC_SECRET_KEY")
ONEWORLDSYNC_USER_GLN = os.getenv("ONEWORLDSYNC_USER_GLN")
ONEWORLDSYNC_CONTENT1_API_URL = os.getenv("ONEWORLDSYNC_CONTENT1_API_URL", "https://content1-api.1worldsync.com")

# Constants
TARGET_MARKET = "US"
BATCH_SIZE = 1000  # Approximate number of records per file to keep under 25MB
OUTPUT_DIR = "us_records"

def ensure_output_directory():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

def write_batch_to_file(batch, batch_num, total_batches):
    """Write a batch of records to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Calculate number of digits needed for zero-padding
    padding = len(str(total_batches))
    # Format batch_num with leading zeros
    padded_batch_num = str(batch_num).zfill(padding)
    filename = f"{OUTPUT_DIR}/us_records_batch_{padded_batch_num}_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(batch, f, indent=2)
    
    file_size_mb = os.path.getsize(filename) / (1024 * 1024)
    print(f"Wrote batch {padded_batch_num} with {len(batch)} records to {filename} ({file_size_mb:.2f} MB)")

def main():
    """Main function to extract US records and write them to JSON files"""
    ensure_output_directory()
    
    # Initialize client
    client = Content1Client(
        app_id=ONEWORLDSYNC_APP_ID,
        secret_key=ONEWORLDSYNC_SECRET_KEY,
        gln=ONEWORLDSYNC_USER_GLN,
        api_url=ONEWORLDSYNC_CONTENT1_API_URL
    )
    
    try:
        # Count total US records
        print(f"Counting products with target market '{TARGET_MARKET}'...")
        criteria = {"targetMarket": TARGET_MARKET}
        total_count = client.count_products(criteria)
        print(f"Total products with target market '{TARGET_MARKET}': {total_count}")
        
        if total_count == 0:
            print("No records found. Exiting.")
            return
        
        # Calculate number of batches
        total_batches = (total_count + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"Will fetch data in approximately {total_batches} batches of {BATCH_SIZE} records each")
        
        # Fetch first batch
        print(f"\nFetching batch 1 of {total_batches}...")
        response = client.fetch_products_by_target_market(TARGET_MARKET, page_size=BATCH_SIZE)
        
        batch_num = 1
        while True:
            if "items" not in response or not response["items"]:
                print("No items found in response")
                break
            
            # Write current batch to file
            write_batch_to_file(response["items"], batch_num, total_batches)
            
            # Check if there are more pages
            if "searchAfter" not in response:
                print("No more pages available. Extraction complete.")
                break
            
            # Fetch next batch
            batch_num += 1
            print(f"\nFetching batch {batch_num} of {total_batches}...")
            response = client.fetch_next_page(response, page_size=BATCH_SIZE, original_criteria=criteria)
        
        print(f"\nExtraction complete. {batch_num} batch(es) written to {OUTPUT_DIR}/ directory")
        
    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except APIError as e:
        print(f"API error: {e}")
        if hasattr(e, 'status_code'):
            print(f"Status code: {e.status_code}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()