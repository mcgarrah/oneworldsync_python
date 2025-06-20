#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example script demonstrating how to use the 1WorldSync Content1 API client.
"""

import os
import json
from dotenv import load_dotenv
from oneworldsync import (
    Content1Client,
    AuthenticationError,
    APIError,
    ProductCriteria,
    DateRangeCriteria,
    SortField,
)

# Load environment variables from .env file
load_dotenv()
ONEWORLDSYNC_APP_ID = os.getenv("ONEWORLDSYNC_APP_ID")
ONEWORLDSYNC_SECRET_KEY = os.getenv("ONEWORLDSYNC_SECRET_KEY")
ONEWORLDSYNC_USER_GLN = os.getenv("ONEWORLDSYNC_USER_GLN")
ONEWORLDSYNC_CONTENT1_API_URL = os.getenv(
    "ONEWORLDSYNC_CONTENT1_API_URL", "https://content1-api.1worldsync.com"
)


def main():
    """Main function demonstrating the 1WorldSync Content1 API client usage"""

    # Initialize client
    client = Content1Client(
        app_id=ONEWORLDSYNC_APP_ID,
        secret_key=ONEWORLDSYNC_SECRET_KEY,
        gln=ONEWORLDSYNC_USER_GLN,
        api_url=ONEWORLDSYNC_CONTENT1_API_URL,
    )

    try:
        # Example 1a: Count products
        print("Counting products...")
        count = client.count_products()
        print(f"Total products available: {count}\n")

        # Example 1b: Count products with criteria
        TARGET_MARKET = "US"
        # Count total US records
        print(f"Counting products with target market '{TARGET_MARKET}'...")
        criteria = {"targetMarket": TARGET_MARKET}
        total_count = client.count_products(criteria)
        print(f"Total products with target market '{TARGET_MARKET}': {total_count}")

        # Example 2: Fetch products by GTIN
        print("\nFetching products by GTIN...")
        # gtins = ["00000000000000"]  # Replace with actual GTINs
        gtins = [
            "04711202220726",
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
            "00079100851744",
        ]
        products = client.fetch_products_by_gtin(gtins)

        # Save the raw product details to a file for inspection
        with open("content1_products.json", "w") as f:
            json.dump(products.to_dict(), f, indent=2)

        print(f"Products saved to content1_products.json")
        
        # Display some product details
        if len(products) > 0:
            print(f"\nFirst few products:")
            for i, product in enumerate(products[:3]):
                print(f"  {i+1}. {product.brand_name} - {product.gtin_name or product.gtin}")
                if product.gpc_category_name:
                    print(f"     Category: {product.gpc_category_name}")
                if product.ingredient_statement:
                    print(f"     Has ingredients: Yes")
                if product.allergen_statement:
                    print(f"     Allergens: {product.allergen_statement[:50]}...")
                print()

        # Example 3: Fetch products with criteria using the builder pattern
        print("\nFetching products with custom criteria...")

        # Create criteria using the builder pattern
        criteria = (
            ProductCriteria()
            .with_target_market("US")
            .with_last_modified_date(
                DateRangeCriteria.between("2023-01-01", "2023-12-31")
            )
            # .with_fields(
            #     include=[
            #         "gtin",
            #         "informationProviderGLN",
            #         "targetMarket",
            #         "lastModifiedDate",
            #         "brandName",
            #         "gpcCategory",
            #     ]
            # )
        )

        products = client.fetch_products(criteria, page_size=10)

        # Process the results - products is now a Content1ProductResults object
        print(f"Found {len(products)} products")

        if len(products) > 0:
            # Display information about the first product
            first_product = products[0]
            print("\nFirst product details:")
            print(f"  GTIN: {first_product.gtin}")
            print(f"  GTIN Name: {first_product.gtin_name}")
            print(f"  Brand: {first_product.brand_name}")
            print(f"  GPC Category: {first_product.gpc_category} - {first_product.gpc_category_name}")
            print(f"  GS1 Trade Item ID: {first_product.gs1_trade_item_identification_key}")
            print(f"  Alternate Classification: {first_product.alternate_classification_code}")
            if first_product.ingredient_statement:
                print(f"  Ingredients: {first_product.ingredient_statement[:100]}...")
            if first_product.allergen_statement:
                print(f"  Allergens: {first_product.allergen_statement}")

            # Check if there are more pages
            if products.search_after:
                print("\nMore pages available. Use fetch_next_page to retrieve them.")

                # Example of fetching the next page
                print("\nFetching next page...")
                next_page = client.fetch_next_page(
                    products, page_size=10, original_criteria=criteria
                )
                print(f"Found {len(next_page)} products on the next page")
        else:
            print("No products found matching the criteria.")

    except AuthenticationError as e:
        print(f"Authentication error: {e}")
    except APIError as e:
        print(f"API error: {e}")
        if hasattr(e, "status_code"):
            print(f"Status code: {e.status_code}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
