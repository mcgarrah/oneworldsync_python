#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for django_nutrition_service.py
"""

import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.append('/path/to/your/django/project')  # Adjust this path to your Django project

# Initialize Django
django.setup()

# Add the current directory to the path so we can import the service
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the NutritionService
from django_nutrition_service import NutritionService

def main():
    """Test the NutritionService"""
    print("Testing Django NutritionService...")
    
    # Initialize the service
    service = NutritionService()
    
    # Test getting nutrition for a specific product
    gtin = "00037600168526"  # Hormel Chorizo
    print(f"\nFetching nutrition for GTIN: {gtin}")
    
    product = service.get_product_nutrition(gtin)
    
    if product:
        print("\nProduct Information:")
        print(f"GTIN: {product.get('gtin')}")
        print(f"Name: {product.get('name')}")
        print(f"Serving Size: {product.get('serving_size', 'N/A')}")
        
        print("\nNutritional Information:")
        print(f"Calories: {product.get('calories', 'N/A')}")
        print(f"Total Fat: {product.get('total_fat_g', 'N/A')}g")
        print(f"Saturated Fat: {product.get('saturated_fat_g', 'N/A')}g")
        print(f"Trans Fat: {product.get('trans_fat_g', 'N/A')}g")
        print(f"Cholesterol: {product.get('cholesterol_mg', 'N/A')}mg")
        print(f"Sodium: {product.get('sodium_mg', 'N/A')}mg")
        print(f"Total Carbs: {product.get('total_carbohydrate_g', 'N/A')}g")
        print(f"Dietary Fiber: {product.get('dietary_fiber_g', 'N/A')}g")
        print(f"Total Sugars: {product.get('total_sugars_g', 'N/A')}g")
        print(f"Protein: {product.get('protein_g', 'N/A')}g")
    else:
        print(f"No product found with GTIN: {gtin}")

if __name__ == "__main__":
    main()
