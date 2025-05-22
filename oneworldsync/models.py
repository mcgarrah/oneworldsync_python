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
        self.gtin = data.get('gtin', '')
        self.item = data.get('item', {})
        
        # Extract structured data for easier access
        self._extracted_data = extract_product_data(data)
    
    @property
    def information_provider_gln(self) -> str:
        """Get the information provider GLN"""
        return self.data.get('informationProviderGLN', '')
    
    @property
    def target_market(self) -> str:
        """Get the target market"""
        return self.data.get('targetMarket', '')
    
    @property
    def last_modified_date(self) -> str:
        """Get the last modified date"""
        return self.data.get('lastModifiedDate', '')
    
    @property
    def brand_name(self) -> str:
        """Get the brand name"""
        return self.item.get('brandName', '')
    
    @property
    def gpc_category(self) -> str:
        """Get the GPC category"""
        return self.item.get('gpcCategory', '')
    
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
            'gpc_category': self.gpc_category
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