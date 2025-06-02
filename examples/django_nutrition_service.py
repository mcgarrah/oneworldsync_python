"""
Django service for retrieving nutritional information from 1WorldSync Content1 API.
"""

import logging
from django.conf import settings
from oneworldsync import Content1Client

logger = logging.getLogger(__name__)

class NutritionService:
    """Service for retrieving nutritional information from 1WorldSync Content1 API."""
    
    # Known food GTINs with nutritional information
    SAMPLE_FOOD_GTINS = [
        "00037600168526",  # Hormel Chorizo
        "00028400083140",  # Doritos
        "00018000428434",  # Cheerios
        "00044000026882",  # Pepsi
        "00079100851744"   # Ritz Crackers
    ]
    
    # Nutrient code mapping
    NUTRIENT_MAPPING = {
        'ENER-': 'calories',
        'FATNLEA': 'total_fat_g',
        'FAT': 'total_fat_g',
        'FASAT': 'saturated_fat_g',
        'FATRN': 'trans_fat_g',
        'CHOL-': 'cholesterol_mg',
        'NA': 'sodium_mg',
        'CHO-': 'total_carbohydrate_g',
        'FIBTSW': 'dietary_fiber_g',
        'FIBR': 'dietary_fiber_g',
        'SUGAR-': 'total_sugars_g',
        'SUGAD': 'added_sugars_g',
        'PRO-': 'protein_g',
        'VITD-': 'vitamin_d_mcg',
        'CA': 'calcium_mg',
        'FE': 'iron_mg',
        'K': 'potassium_mg'
    }
    
    def __init__(self):
        """Initialize the service with credentials from Django settings."""
        self.client = Content1Client(
            app_id=getattr(settings, 'ONEWORLDSYNC_APP_ID', None),
            secret_key=getattr(settings, 'ONEWORLDSYNC_SECRET_KEY', None),
            gln=getattr(settings, 'ONEWORLDSYNC_USER_GLN', None)
        )
    
    def get_product_nutrition(self, gtin):
        """Get nutritional information for a product by GTIN."""
        try:
            response = self.client.fetch_products_by_gtin([gtin])
            
            if not response or 'items' not in response or not response['items']:
                return None
            
            product_data = response['items'][0]
            
            # Extract basic product info
            product_info = self._extract_product_info(product_data)
            
            # Extract nutritional info
            nutrition_info = self._extract_nutritional_info(product_data)
            
            # Combine the information
            product_info.update(nutrition_info)
            
            return product_info
        except Exception as e:
            logger.error(f"Error fetching product nutrition: {e}")
            return None
    
    def get_sample_food_products(self):
        """Get sample food products with nutritional information."""
        try:
            response = self.client.fetch_products_by_gtin(self.SAMPLE_FOOD_GTINS)
            
            if not response or 'items' not in response:
                return []
            
            products = []
            for product_data in response['items']:
                # Extract basic product info
                product_info = self._extract_product_info(product_data)
                
                # Extract nutritional info
                nutrition_info = self._extract_nutritional_info(product_data)
                
                # Combine the information
                product_info.update(nutrition_info)
                
                products.append(product_info)
            
            return products
        except Exception as e:
            logger.error(f"Error fetching food products: {e}")
            return []
    
    def _extract_product_info(self, product_data):
        """Extract basic product information."""
        product_info = {
            'gtin': product_data.get('gtin', ''),
            'source': '1WorldSync'
        }
        
        # Extract item data
        item = product_data.get('item', {})
        
        # Get brand name
        product_info['name'] = item.get('brandName', '')
        
        return product_info
    
    def _extract_nutritional_info(self, product_data):
        """Extract nutritional information from product data."""
        nutrition_info = {}
        
        try:
            item_data = product_data.get('item', {})
            
            # In this product, nutritional info is in nutrientInformation
            nutrient_info = item_data.get('nutrientInformation', [])
            
            for info in nutrient_info:
                # Extract serving size
                serving_size = info.get('servingSize', [])
                if serving_size and len(serving_size) > 0:
                    value = serving_size[0].get('value', '')
                    unit = serving_size[0].get('qual', '')
                    nutrition_info['serving_size'] = f"{value} {unit}".strip()
                
                # Extract servings per package
                servings_per_package = info.get('servingsPerPackageDescription', [])
                if servings_per_package and len(servings_per_package) > 0:
                    nutrition_info['servings_per_container'] = servings_per_package[0].get('value', '')
                
                # Extract nutrient details
                nutrient_details = info.get('nutrientDetail', [])
                
                for nutrient in nutrient_details:
                    nutrient_type = nutrient.get('nutrientTypeCode', '')
                    
                    # Get quantity
                    quantity = nutrient.get('quantityContained', [])
                    value = quantity[0].get('value', '') if quantity else ''
                    
                    # Map to Django model fields
                    field_name = self.NUTRIENT_MAPPING.get(nutrient_type)
                    if field_name:
                        nutrition_info[field_name] = value
                    
                    # Get daily value percentage
                    daily_value = nutrient.get('dailyValueIntakePercent', '')
                    if daily_value and field_name:
                        nutrition_info[f"{field_name}_dv"] = daily_value
        
        except Exception as e:
            logger.error(f"Error extracting nutritional info: {e}")
        
        return nutrition_info