"""
Models for the 1WorldSync API

This module defines data models for the 1WorldSync API responses.
"""

from typing import Dict, List, Any, Optional, Union
from .utils import extract_product_data, get_primary_image, format_dimensions


class Product:
    """
    Model representing a product from the 1WorldSync API
    """
    
    def __init__(self, data):
        """
        Initialize a product from API data
        
        Args:
            data (dict): Product data from the API
        """
        self.data = data
        self.item = data.get('item', {})
        
        # Extract structured data for easier access
        self._extracted_data = extract_product_data(data)
    
    @property
    def item_id(self) -> str:
        """Get the primary item ID"""
        if self._extracted_data.get('item_id'):
            return self._extracted_data['item_id']
            
        identifiers = self.item.get('itemIdentificationInformation', {}).get('itemIdentifier', [])
        for identifier in identifiers:
            if identifier.get('isPrimary') == 'true':
                return identifier.get('itemId')
        return None
    
    @property
    def gtin(self) -> str:
        """Get the GTIN (Global Trade Item Number)"""
        return self._extracted_data.get('gtin', '')
    
    @property
    def brand_name(self) -> str:
        """Get the brand name"""
        if self._extracted_data.get('brand_name'):
            return self._extracted_data['brand_name']
            
        try:
            info = self.item.get('tradeItemInformation', [])[0]
            desc_module = info.get('tradeItemDescriptionModule', {})
            desc_info = desc_module.get('tradeItemDescriptionInformation', [])[0]
            return desc_info.get('brandNameInformation', {}).get('brandName')
        except (IndexError, KeyError, TypeError):
            return None
    
    @property
    def product_name(self) -> str:
        """Get the product name"""
        if self._extracted_data.get('product_name'):
            return self._extracted_data['product_name']
            
        try:
            info = self.item.get('tradeItemInformation', [])[0]
            desc_module = info.get('tradeItemDescriptionModule', {})
            desc_info = desc_module.get('tradeItemDescriptionInformation', [])[0]
            reg_names = desc_info.get('regulatedProductName', [])
            if reg_names:
                return reg_names[0].get('statement', {}).get('values', [])[0].get('value')
        except (IndexError, KeyError, TypeError):
            return None
    
    @property
    def description(self) -> str:
        """Get the product description"""
        if self._extracted_data.get('description'):
            return self._extracted_data['description']
            
        try:
            info = self.item.get('tradeItemInformation', [])[0]
            desc_module = info.get('tradeItemDescriptionModule', {})
            desc_info = desc_module.get('tradeItemDescriptionInformation', [])[0]
            desc = desc_info.get('additionalTradeItemDescription', {})
            return desc.get('values', [])[0].get('value')
        except (IndexError, KeyError, TypeError):
            return None
    
    @property
    def images(self) -> List[Dict[str, Any]]:
        """Get product images"""
        if self._extracted_data.get('images'):
            return self._extracted_data['images']
            
        try:
            info = self.item.get('tradeItemInformation', [])[0]
            file_module = info.get('referencedFileDetailInformationModule', {})
            file_headers = file_module.get('referencedFileHeader', [])
            
            images = []
            for file_header in file_headers:
                if file_header.get('referencedFileTypeCode', {}).get('value') == 'PRODUCT_IMAGE':
                    images.append({
                        'url': file_header.get('uniformResourceIdentifier'),
                        'is_primary': file_header.get('isPrimaryFile', {}).get('value') == 'true'
                    })
            return images
        except (IndexError, KeyError, TypeError):
            return []
    
    @property
    def primary_image_url(self) -> str:
        """Get the primary image URL"""
        return get_primary_image(self._extracted_data)
    
    @property
    def dimensions(self) -> Dict[str, Dict[str, str]]:
        """Get product dimensions"""
        if self._extracted_data.get('dimensions'):
            return self._extracted_data['dimensions']
            
        try:
            info = self.item.get('tradeItemInformation', [])[0]
            measurements_group = info.get('tradeItemMeasurementsModuleGroup', [])[0]
            measurements_module = measurements_group.get('tradeItemMeasurementsModule', {})
            measurements = measurements_module.get('tradeItemMeasurements', {})
            
            return {
                'height': {
                    'value': measurements.get('height', {}).get('value'),
                    'unit': measurements.get('height', {}).get('qual')
                },
                'width': {
                    'value': measurements.get('width', {}).get('value'),
                    'unit': measurements.get('width', {}).get('qual')
                },
                'depth': {
                    'value': measurements.get('depth', {}).get('value'),
                    'unit': measurements.get('depth', {}).get('qual')
                }
            }
        except (IndexError, KeyError, TypeError):
            return {}
    
    @property
    def formatted_dimensions(self) -> str:
        """Get formatted dimensions as a string"""
        return format_dimensions(self.dimensions)
    
    @property
    def gpc_code(self) -> str:
        """Get the GPC (Global Product Classification) code"""
        return self._extracted_data.get('gpc_code', '')
    
    @property
    def category(self) -> str:
        """Get the product category"""
        return self._extracted_data.get('category', '')
    
    @property
    def ingredients(self) -> str:
        """Get the product ingredients"""
        return self._extracted_data.get('ingredients', '')
    
    @property
    def country_of_origin(self) -> str:
        """Get the country of origin"""
        return self._extracted_data.get('country_of_origin', '')
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the product to a dictionary with all extracted data
        
        Returns:
            dict: Dictionary representation of the product
        """
        return {
            'item_id': self.item_id,
            'gtin': self.gtin,
            'brand_name': self.brand_name,
            'product_name': self.product_name,
            'description': self.description,
            'primary_image_url': self.primary_image_url,
            'images': self.images,
            'dimensions': self.dimensions,
            'formatted_dimensions': self.formatted_dimensions,
            'gpc_code': self.gpc_code,
            'category': self.category,
            'ingredients': self.ingredients,
            'country_of_origin': self.country_of_origin
        }
    
    def __str__(self):
        """String representation of the product"""
        return f"{self.brand_name} - {self.product_name} ({self.item_id})"


class SearchResults:
    """
    Model representing search results from the 1WorldSync API
    """
    
    def __init__(self, data):
        """
        Initialize search results from API data
        
        Args:
            data (dict): Search results data from the API
        """
        self.data = data
        self.response_code = data.get('responseCode')
        self.response_message = data.get('responseMessage')
        self.total_results = int(data.get('totalNumOfResults', '0'))
        self.next_cursor = data.get('nextCursorMark')
        
        # Parse products
        self.products = []
        for result in data.get('results', []):
            self.products.append(Product(result))
    
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
        Convert the search results to a dictionary
        
        Returns:
            dict: Dictionary representation of the search results
        """
        return {
            'metadata': {
                'response_code': self.response_code,
                'response_message': self.response_message,
                'total_results': self.total_results,
                'next_cursor': self.next_cursor
            },
            'products': [product.to_dict() for product in self.products]
        }