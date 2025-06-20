"""
Models for the 1WorldSync Content1 API

This module defines data models for the 1WorldSync Content1 API responses.
"""

from typing import Dict, List, Any, Optional, Union
from .utils import extract_product_data, get_primary_image, format_dimensions


class Content1Product:
    """
    Model representing a product from the 1WorldSync Content1 API
    """
    
    def __init__(self, data):
        """
        Initialize a product from API data
        
        Args:
            data (dict): Product data from the API
        """
        self.data = data
        self.item = data.get('item', {})
        self.gtin = self.item.get('gtin', data.get('gtin', ''))
        
        # Extract structured data for easier access
        self._extracted_data = extract_product_data(data)
    
    @property
    def information_provider_gln(self) -> str:
        """Get the information provider GLN"""
        return self.item.get('informationProviderGLN', self.data.get('informationProviderGLN', ''))
    
    @property
    def target_market(self) -> str:
        """Get the target market"""
        return self.item.get('targetMarket', self.data.get('targetMarket', ''))
    
    @property
    def last_modified_date(self) -> str:
        """Get the last modified date"""
        return self.item.get('lastModifiedDate', self.data.get('lastModifiedDate', ''))
    
    @property
    def brand_name(self) -> str:
        """Get the brand name"""
        return self.item.get('brandName', '')
    
    @property
    def gpc_category(self) -> str:
        """Get the GPC category"""
        gpc = self.item.get('globalClassificationCategory', {})
        if isinstance(gpc, dict):
            return gpc.get('code', '')
        return self.item.get('gpcCategory', '')
    
    @property
    def gpc_category_name(self) -> str:
        """Get the GPC category name"""
        gpc = self.item.get('globalClassificationCategory', {})
        if isinstance(gpc, dict):
            return gpc.get('name', '')
        return ''
    
    @property
    def gtin_name(self) -> str:
        """Get the GTIN name"""
        gtin_name = self.item.get('gtinName', [])
        if gtin_name and isinstance(gtin_name, list) and len(gtin_name) > 0:
            return gtin_name[0].get('value', '')
        return ''
    
    @property
    def gs1_trade_item_identification_key(self) -> Dict[str, str]:
        """Get the GS1 trade item identification key"""
        gs1_key = self.item.get('gs1TradeItemIdentificationKey', [])
        if gs1_key and isinstance(gs1_key, list) and len(gs1_key) > 0:
            return {
                'code': gs1_key[0].get('code', ''),
                'value': gs1_key[0].get('value', '')
            }
        return {'code': '', 'value': ''}
    
    @property
    def alternate_classification_code(self) -> str:
        """Get the alternate classification code"""
        alt_class = self.item.get('alternateClassification', [])
        if alt_class and isinstance(alt_class, list) and len(alt_class) > 0:
            return alt_class[0].get('code', '')
        return ''
    
    @property
    def ingredient_statement(self) -> str:
        """Get the ingredient statement for food/beverage items"""
        ingredients = self.item.get('ingredientStatement', [])
        if ingredients and isinstance(ingredients, list) and len(ingredients) > 0:
            statements = ingredients[0].get('statement', [])
            if statements and isinstance(statements, list) and len(statements) > 0:
                return statements[0].get('value', '')
        return ''
    
    @property
    def allergen_statement(self) -> str:
        """Get the allergen statement for food/beverage items"""
        allergen_info = self.item.get('allergenRelatedInformation', [])
        if allergen_info and isinstance(allergen_info, list) and len(allergen_info) > 0:
            statements = allergen_info[0].get('allergenStatement', [])
            if statements and isinstance(statements, list) and len(statements) > 0:
                return statements[0].get('value', '')
        return ''
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the product to a dictionary with all extracted data
        
        Returns:
            dict: Dictionary representation of the product
        """
        return {
            'gtin': self.gtin,
            'information_provider_gln': self.information_provider_gln,
            'target_market': self.target_market,
            'last_modified_date': self.last_modified_date,
            'brand_name': self.brand_name,
            'gpc_category': self.gpc_category,
            'gpc_category_name': self.gpc_category_name,
            'gtin_name': self.gtin_name,
            'gs1_trade_item_identification_key': self.gs1_trade_item_identification_key,
            'alternate_classification_code': self.alternate_classification_code,
            'ingredient_statement': self.ingredient_statement,
            'allergen_statement': self.allergen_statement
        }
    
    def __str__(self):
        """String representation of the product"""
        return f"{self.brand_name} - {self.gtin} ({self.target_market})"


class Content1ProductResults:
    """
    Model representing product results from the 1WorldSync Content1 API
    """
    
    def __init__(self, data):
        """
        Initialize product results from API data
        
        Args:
            data (dict): Product results data from the API
        """
        self.data = data
        self.search_after = data.get('searchAfter')
        
        # Parse products
        self.products = []
        for item in data.get('items', []):
            self.products.append(Content1Product(item))
    
    def __len__(self):
        """Get the number of products in the results"""
        return len(self.products)
    
    def __iter__(self):
        """Iterate through products"""
        return iter(self.products)
    
    def __getitem__(self, index):
        """Get a product by index"""
        return self.products[index]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the product results to a dictionary
        
        Returns:
            dict: Dictionary representation of the product results
        """
        return {
            'metadata': {
                'search_after': self.search_after
            },
            'products': [product.to_dict() for product in self.products]
        }


class Content1Hierarchy:
    """
    Model representing a product hierarchy from the 1WorldSync Content1 API
    """
    
    def __init__(self, data):
        """
        Initialize a hierarchy from API data
        
        Args:
            data (dict): Hierarchy data from the API
        """
        self.data = data
        self.gtin = data.get('gtin', '')
        self.information_provider_gln = data.get('informationProviderGLN', '')
        self.target_market = data.get('targetMarket', '')
        self.hierarchy = data.get('hierarchy', [])
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the hierarchy to a dictionary
        
        Returns:
            dict: Dictionary representation of the hierarchy
        """
        return {
            'gtin': self.gtin,
            'information_provider_gln': self.information_provider_gln,
            'target_market': self.target_market,
            'hierarchy': self.hierarchy
        }
    
    def __str__(self):
        """String representation of the hierarchy"""
        return f"Hierarchy for GTIN {self.gtin} in {self.target_market}"


class Content1HierarchyResults:
    """
    Model representing hierarchy results from the 1WorldSync Content1 API
    """
    
    def __init__(self, data):
        """
        Initialize hierarchy results from API data
        
        Args:
            data (dict): Hierarchy results data from the API
        """
        self.data = data
        self.search_after = data.get('searchAfter')
        
        # Parse hierarchies
        self.hierarchies = []
        for item in data.get('hierarchies', []):
            self.hierarchies.append(Content1Hierarchy(item))
    
    def __len__(self):
        """Get the number of hierarchies in the results"""
        return len(self.hierarchies)
    
    def __iter__(self):
        """Iterate through hierarchies"""
        return iter(self.hierarchies)
    
    def __getitem__(self, index):
        """Get a hierarchy by index"""
        return self.hierarchies[index]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the hierarchy results to a dictionary
        
        Returns:
            dict: Dictionary representation of the hierarchy results
        """
        return {
            'metadata': {
                'search_after': self.search_after
            },
            'hierarchies': [hierarchy.to_dict() for hierarchy in self.hierarchies]
        }