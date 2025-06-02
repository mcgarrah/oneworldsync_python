#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple example for retrieving food product data with nutritional information
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

# Known food GTINs with nutritional information
SAMPLE_FOOD_GTINS = [
    "00037600168526",  # Hormel Chorizo
    "00028400083140",  # Doritos
    "00018000428434",  # Cheerios
    "00044000026882",  # Pepsi
    "00079100851744"   # Ritz Crackers
]

def main():
    """Main function demonstrating how to retrieve nutritional information"""
    
    # Initialize client
    client = Content1Client(
        app_id=ONEWORLDSYNC_APP_ID,
        secret_key=ONEWORLDSYNC_SECRET_KEY,
        gln=ONEWORLDSYNC_USER_GLN
    )
    
    # Fetch a single product by GTIN
    gtin = SAMPLE_FOOD_GTINS[0]  # Hormel Chorizo
    print(f"Fetching product with GTIN: {gtin}")
    
    response = client.fetch_products_by_gtin([gtin])
    
    if response and 'items' in response and response['items']:
        product = response['items'][0]
        
        # Print basic product info
        print("\nProduct Information:")
        print(f"GTIN: {product.get('gtin')}")
        
        # Extract item data
        item = product.get('item', {})
        
        # Get brand name
        brand_name = item.get('brandName', 'Unknown')
        print(f"Brand: {brand_name}")
        
        # Look for nutritional information
        print("\nSearching for nutritional information...")
        
        # In this product, nutritional info is in nutrientInformation
        nutrient_info = item.get('nutrientInformation', [])
        
        if nutrient_info:
            print(f"Found nutrient information!")
            
            for info in nutrient_info:
                # Extract serving size
                serving_size = info.get('servingSize', [])
                if serving_size and len(serving_size) > 0:
                    value = serving_size[0].get('value', '')
                    unit = serving_size[0].get('qual', '')
                    print(f"Serving Size: {value} {unit}")
                
                # Extract nutrient details
                nutrient_details = info.get('nutrientDetail', [])
                
                if nutrient_details:
                    print(f"\nNutrient Facts ({len(nutrient_details)} found):")
                    
                    for nutrient in nutrient_details:
                        nutrient_type = nutrient.get('nutrientTypeCode', '')
                        
                        # Get quantity
                        quantity = nutrient.get('quantityContained', [])
                        value = quantity[0].get('value', '') if quantity else ''
                        unit = quantity[0].get('qual', '') if quantity else ''
                        
                        # Get daily value percentage
                        daily_value = nutrient.get('dailyValueIntakePercent', '')
                        dv_str = f" ({daily_value}% DV)" if daily_value else ""
                        
                        # Map nutrient codes to readable names
                        nutrient_names = {
                            'ENER-': 'Calories',
                            'FATNLEA': 'Total Fat',
                            'FASAT': 'Saturated Fat',
                            'FATRN': 'Trans Fat',
                            'CHOL-': 'Cholesterol',
                            'NA': 'Sodium',
                            'CHO-': 'Total Carbohydrate',
                            'FIBTSW': 'Dietary Fiber',
                            'SUGAR-': 'Total Sugars',
                            'SUGAD': 'Added Sugars',
                            'PRO-': 'Protein',
                            'VITD-': 'Vitamin D',
                            'CA': 'Calcium',
                            'FE': 'Iron',
                            'K': 'Potassium'
                        }
                        
                        nutrient_name = nutrient_names.get(nutrient_type, nutrient_type)
                        print(f"  {nutrient_name}: {value} {unit}{dv_str}")
                        
                        # Map to Django model fields
                        if nutrient_type == 'ENER-':
                            print(f"  Django field: calories = {value}")
                        elif nutrient_type == 'FATNLEA':
                            print(f"  Django field: total_fat_g = {value}")
                        elif nutrient_type == 'FASAT':
                            print(f"  Django field: saturated_fat_g = {value}")
                        elif nutrient_type == 'FATRN':
                            print(f"  Django field: trans_fat_g = {value}")
                        elif nutrient_type == 'CHOL-':
                            print(f"  Django field: cholesterol_mg = {value}")
                        elif nutrient_type == 'NA':
                            print(f"  Django field: sodium_mg = {value}")
                        elif nutrient_type == 'CHO-':
                            print(f"  Django field: total_carbohydrate_g = {value}")
                        elif nutrient_type == 'FIBTSW':
                            print(f"  Django field: dietary_fiber_g = {value}")
                        elif nutrient_type == 'SUGAR-':
                            print(f"  Django field: total_sugars_g = {value}")
                        elif nutrient_type == 'PRO-':
                            print(f"  Django field: protein_g = {value}")
        else:
            print("No nutritional information found in this product.")
    else:
        print(f"No product found with GTIN: {gtin}")

if __name__ == "__main__":
    main()