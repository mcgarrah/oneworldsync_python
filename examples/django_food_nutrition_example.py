#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Django integration example for retrieving food/beverage product data with nutritional information
using the 1WorldSync Content1 API client.
"""

import os
import json
from dotenv import load_dotenv
from oneworldsync import Content1Client

# Load environment variables from .env file
load_dotenv()
ONEWORLDSYNC_APP_ID = os.getenv("ONEWORLDSYNC_APP_ID")
ONEWORLDSYNC_SECRET_KEY = os.getenv("ONEWORLDSYNC_SECRET_KEY")
ONEWORLDSYNC_USER_GLN = os.getenv("ONEWORLDSYNC_USER_GLN")

# GPC Segment codes for Food/Beverage categories
FOOD_BEVERAGE_GPC_SEGMENTS = {
    "50000000": "Food/Beverage/Tobacco",
    "50030000": "Food - Shelf Stable",
    "50190000": "Beverages"
}

def extract_nutritional_info(product_data):
    """Extract nutritional information from product data"""
    nutritional_info = {}
    
    try:
        # Debug the structure of product_data
        print(f"Product GTIN: {product_data.get('gtin')}")
        
        item_data = product_data.get('item', {})
        
        # Debug item structure
        if not item_data:
            print("No item data found")
            return nutritional_info
            
        trade_item_info = item_data.get('tradeItemInformation', [])
        if not trade_item_info:
            print("No tradeItemInformation found")
            return nutritional_info
            
        # Look for nutritional information
        for info in trade_item_info:
            nutritional_modules = info.get('nutritionalInformationModule', [])
            
            if not nutritional_modules:
                continue
                
            print(f"Found nutritionalInformationModule")
            
            for module in nutritional_modules:
                # Extract serving size
                serving_size = module.get('servingSize', {})
                if serving_size:
                    nutritional_info['serving_size'] = {
                        'value': serving_size.get('value', ''),
                        'unit': serving_size.get('qual', '')
                    }
                
                # Extract nutrient facts
                nutrient_facts = module.get('nutrientFacts', [])
                
                if not nutrient_facts:
                    print("No nutrient facts found")
                    continue
                    
                print(f"Found {len(nutrient_facts)} nutrient facts")
                
                for fact in nutrient_facts:
                    nutrient_type = fact.get('nutrientTypeCode', {}).get('value', '')
                    if not nutrient_type:
                        continue
                    
                    print(f"Found nutrient: {nutrient_type}")
                    
                    quantity = fact.get('quantityContained', {})
                    value = quantity.get('value', '')
                    unit = quantity.get('qual', '')
                    
                    # Map common nutrient codes
                    nutrient_mapping = {
                        'ENER-': 'calories',
                        'FAT': 'total_fat',
                        'FASAT': 'saturated_fat',
                        'FATRN': 'trans_fat',
                        'CHOL': 'cholesterol',
                        'NA': 'sodium',
                        'CHO-': 'total_carbohydrate',
                        'FIBR': 'dietary_fiber',
                        'SUGAR': 'total_sugars',
                        'PRO-': 'protein'
                    }
                    
                    nutrient_name = nutrient_mapping.get(nutrient_type, nutrient_type)
                    nutritional_info[nutrient_name] = {
                        'value': value,
                        'unit': unit
                    }
                    
                    # Get daily value percentage
                    daily_value = fact.get('dailyValueIntakePercent', '')
                    if daily_value:
                        nutritional_info[f"{nutrient_name}_dv"] = daily_value
    
    except Exception as e:
        print(f"Error extracting nutritional data: {e}")
    
    return nutritional_info

def fetch_food_products(client, segment_code="50030000", page_size=5):
    """Fetch food/beverage products from the Content1 API"""
    try:
        # Create criteria for food products with more detailed fields
        criteria = {
            "targetMarket": "US",
            "gpcSegmentCode": segment_code,
            "fields": {
                "include": [
                    "gtin", 
                    "informationProviderGLN",
                    "targetMarket",
                    "brandName",
                    "gpcCategory",
                    "tradeItemDescriptions",
                    "tradeItemInformation"
                ]
            }
        }
        
        # Try with specific GTINs known to have nutritional info
        sample_gtins = [
            "00037600168526",
            "00028400083140",
            "00018000428434",
            "00044000026882",
            "00079100851744"
        ]
        
        criteria = {
            "gtin": sample_gtins,
            "fields": {
                "include": [
                    "gtin", 
                    "informationProviderGLN",
                    "targetMarket",
                    "brandName",
                    "gpcCategory",
                    "tradeItemDescriptions",
                    "tradeItemInformation"
                ]
            }
        }
        
        print("Fetching products with criteria:", json.dumps(criteria, indent=2))
        response = client.fetch_products(criteria, page_size=page_size)
        
        if not response or 'items' not in response:
            print("No items found in response")
            return []
            
        print(f"Found {len(response['items'])} items in response")
        
        products = []
        for product_data in response['items']:
            # Extract GTIN
            gtin = product_data.get('gtin', '')
            
            # Extract nutritional information
            nutritional_info = extract_nutritional_info(product_data)
            
            # Map to Django model fields
            product = {
                'gtin': gtin,
                'source': '1WorldSync'
            }
            
            # Add nutritional information
            if 'calories' in nutritional_info:
                product['calories'] = nutritional_info['calories']['value']
            if 'total_fat' in nutritional_info:
                product['total_fat_g'] = nutritional_info['total_fat']['value']
            if 'sodium' in nutritional_info:
                product['sodium_mg'] = nutritional_info['sodium']['value']
            if 'total_carbohydrate' in nutritional_info:
                product['total_carbohydrate_g'] = nutritional_info['total_carbohydrate']['value']
            if 'protein' in nutritional_info:
                product['protein_g'] = nutritional_info['protein']['value']
            
            products.append(product)
        
        return products
    
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []

def main():
    """Main function demonstrating the 1WorldSync Content1 API for food products"""
    client = Content1Client(
        app_id=ONEWORLDSYNC_APP_ID,
        secret_key=ONEWORLDSYNC_SECRET_KEY,
        gln=ONEWORLDSYNC_USER_GLN
    )
    
    print("Fetching food products...")
    products = fetch_food_products(client)
    
    if products:
        print(f"Found {len(products)} products")
        for product in products:
            print(f"\nGTIN: {product.get('gtin')}")
            print(f"Calories: {product.get('calories', 'N/A')}")
            print(f"Total Fat: {product.get('total_fat_g', 'N/A')}g")
            print(f"Sodium: {product.get('sodium_mg', 'N/A')}mg")
            print(f"Total Carbs: {product.get('total_carbohydrate_g', 'N/A')}g")
            print(f"Protein: {product.get('protein_g', 'N/A')}g")
    else:
        print("No products found")

if __name__ == "__main__":
    main()