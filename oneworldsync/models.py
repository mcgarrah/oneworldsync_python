"""
Models for the 1WorldSync API

This module defines data models for the 1WorldSync API responses.
"""


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
    
    @property
    def item_id(self):
        """Get the primary item ID"""
        identifiers = self.item.get('itemIdentificationInformation', {}).get('itemIdentifier', [])
        for identifier in identifiers:
            if identifier.get('isPrimary') == 'true':
                return identifier.get('itemId')
        return None
    
    @property
    def brand_name(self):
        """Get the brand name"""
        try:
            info = self.item.get('tradeItemInformation', [])[0]
            desc_module = info.get('tradeItemDescriptionModule', {})
            desc_info = desc_module.get('tradeItemDescriptionInformation', [])[0]
            return desc_info.get('brandNameInformation', {}).get('brandName')
        except (IndexError, KeyError, TypeError):
            return None
    
    @property
    def product_name(self):
        """Get the product name"""
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
    def description(self):
        """Get the product description"""
        try:
            info = self.item.get('tradeItemInformation', [])[0]
            desc_module = info.get('tradeItemDescriptionModule', {})
            desc_info = desc_module.get('tradeItemDescriptionInformation', [])[0]
            desc = desc_info.get('additionalTradeItemDescription', {})
            return desc.get('values', [])[0].get('value')
        except (IndexError, KeyError, TypeError):
            return None
    
    @property
    def images(self):
        """Get product images"""
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
    def dimensions(self):
        """Get product dimensions"""
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