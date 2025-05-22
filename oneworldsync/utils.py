"""
Utility functions for the 1WorldSync Content1 API client
"""

import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Union

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_timestamp(dt=None):
    """
    Format a datetime object as a timestamp for the 1WorldSync API
    
    Args:
        dt (datetime, optional): Datetime object to format. Defaults to current UTC time.
        
    Returns:
        str: Formatted timestamp
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


def parse_timestamp(timestamp_str):
    """
    Parse a timestamp string from the 1WorldSync API
    
    Args:
        timestamp_str (str): Timestamp string in ISO 8601 format
        
    Returns:
        datetime: Parsed datetime object
    """
    return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')


def pretty_print_json(data):
    """
    Pretty print JSON data
    
    Args:
        data (dict): JSON data to print
    """
    print(json.dumps(data, indent=2))


def extract_nested_value(data, path, default=None):
    """
    Extract a value from a nested dictionary using a path
    
    Args:
        data (dict): Dictionary to extract from
        path (list): List of keys to traverse
        default: Value to return if path doesn't exist
        
    Returns:
        The value at the path or the default value
    """
    current = data
    
    try:
        for key in path:
            if isinstance(current, dict):
                current = current.get(key)
            elif isinstance(current, list) and isinstance(key, int) and 0 <= key < len(current):
                current = current[key]
            else:
                return default
            
            if current is None:
                return default
        
        return current
    except (KeyError, IndexError, TypeError):
        return default


def get_nested_dict_value(data: Dict, path: str, default: Any = None) -> Any:
    """
    Extract a value from a nested dictionary using a dot-separated path
    
    Args:
        data (dict): Dictionary to extract from
        path (str): Dot-separated path (e.g., "item.tradeItemInformation.0.tradeItemDescriptionModule")
        default: Value to return if path doesn't exist
        
    Returns:
        The value at the path or the default value
    """
    if not data or not isinstance(data, dict):
        return default
        
    parts = path.split('.')
    current = data
    
    for part in parts:
        # Handle array indices
        if part.isdigit() and isinstance(current, list):
            index = int(part)
            if 0 <= index < len(current):
                current = current[index]
            else:
                return default
        elif isinstance(current, dict):
            current = current.get(part)
        else:
            return default
            
        if current is None:
            return default
            
    return current


def extract_product_data(product_data: Dict) -> Dict:
    """
    Extract relevant product data from a 1WorldSync product object based on the Swagger Search schema.
    
    Args:
        product_data (dict): A product data dictionary from the 1WorldSync Search REST API
        
    Returns:
        dict: A dictionary with structured product data
    """
    # Initialize with default values
    extracted_data = {
        'gtin': '',
        'brand_name': '',
        'product_name': '',
        'description': '',
        'manufacturer': '',
        'image_url': '',
        'category': '',
        'subcategory': '',
        'gpc_code': '',
        'ingredients': '',
        'dimensions': {},
        'country_of_origin': '',
        'allergen_info': [],
        'item_id': '',
        'images': []
    }
    
    try:
        item = product_data.get('item', {})
        
        # Extract GTIN (item identifier)
        identifiers = get_nested_dict_value(item, 'itemIdentificationInformation.itemIdentifier', [])
        for identifier in identifiers:
            if identifier.get('itemIdType', {}).get('value') == 'GTIN':
                extracted_data['gtin'] = identifier.get('itemId', '')
                break
        
        # Extract item reference ID
        item_ref_info = get_nested_dict_value(item, 'itemIdentificationInformation.itemReferenceIdInformation', {})
        extracted_data['item_id'] = item_ref_info.get('itemReferenceId', '')
        
        # Extract trade item information
        trade_item_info = get_nested_dict_value(item, 'tradeItemInformation', [])
        if trade_item_info:
            # Extract brand name and product name
            for info in trade_item_info:
                desc_info = get_nested_dict_value(info, 'tradeItemDescriptionModule.tradeItemDescriptionInformation', [])
                for desc in desc_info:
                    # Brand name
                    brand_info = desc.get('brandNameInformation', {})
                    if brand_info:
                        extracted_data['brand_name'] = brand_info.get('brandName', '')
                    
                    # Product name
                    reg_names = desc.get('regulatedProductName', [])
                    for reg_name in reg_names:
                        values = get_nested_dict_value(reg_name, 'statement.values', [])
                        for value in values:
                            if value.get('value'):
                                extracted_data['product_name'] = value.get('value')
                                break
                    
                    # Description
                    add_desc = get_nested_dict_value(desc, 'additionalTradeItemDescription.values', [])
                    for desc_val in add_desc:
                        if desc_val.get('value'):
                            extracted_data['description'] = desc_val.get('value')
                            break
                
                # Extract images
                file_module = get_nested_dict_value(info, 'referencedFileDetailInformationModule', {})
                file_headers = file_module.get('referencedFileHeader', [])
                
                for file_header in file_headers:
                    file_type = get_nested_dict_value(file_header, 'referencedFileTypeCode.value', '')
                    if file_type == 'PRODUCT_IMAGE':
                        uri = file_header.get('uniformResourceIdentifier', '')
                        is_primary = get_nested_dict_value(file_header, 'isPrimaryFile.value', '') == 'true'
                        
                        image_data = {
                            'url': uri,
                            'is_primary': is_primary
                        }
                        
                        extracted_data['images'].append(image_data)
                        
                        # Set primary image as the main image URL
                        if is_primary and uri:
                            extracted_data['image_url'] = uri
                
                # Extract dimensions
                measurement_groups = get_nested_dict_value(info, 'tradeItemMeasurementsModuleGroup', [])
                for group in measurement_groups:
                    measurements = get_nested_dict_value(group, 'tradeItemMeasurementsModule.tradeItemMeasurements', {})
                    if measurements:
                        # Height
                        height = measurements.get('height', {})
                        if height:
                            extracted_data['dimensions']['height'] = {
                                'value': height.get('value', ''),
                                'unit': height.get('qual', '')
                            }
                        
                        # Width
                        width = measurements.get('width', {})
                        if width:
                            extracted_data['dimensions']['width'] = {
                                'value': width.get('value', ''),
                                'unit': width.get('qual', '')
                            }
                        
                        # Depth
                        depth = measurements.get('depth', {})
                        if depth:
                            extracted_data['dimensions']['depth'] = {
                                'value': depth.get('value', ''),
                                'unit': depth.get('qual', '')
                            }
                
                # Extract ingredients
                ingredient_modules = get_nested_dict_value(info, 'foodAndBeverageIngredientModule', [])
                for module in ingredient_modules:
                    statements = get_nested_dict_value(module, 'ingredientStatement', [])
                    for statement in statements:
                        values = get_nested_dict_value(statement, 'statement.values', [])
                        for value in values:
                            if value.get('value'):
                                extracted_data['ingredients'] = value.get('value')
                                break
                
                # Extract country of origin
                place_module = get_nested_dict_value(info, 'placeOfItemActivityModule', {})
                countries = get_nested_dict_value(place_module, 'placeOfProductActivity.countryOfOrigin', [])
                for country in countries:
                    country_code = get_nested_dict_value(country, 'countryCode.value', '')
                    if country_code:
                        extracted_data['country_of_origin'] = country_code
                        break
        
        # Extract GPC code and category
        product_categories = get_nested_dict_value(item, 'productCategory', [])
        for category in product_categories:
            scheme = get_nested_dict_value(category, 'productCategoryScheme.value', '')
            if scheme == 'GPC':
                category_codes = category.get('productCategoryCodes', [])
                for code in category_codes:
                    gpc_code = get_nested_dict_value(code, 'productCategoryCode.value', '')
                    if gpc_code:
                        extracted_data['gpc_code'] = gpc_code
                        
                        # Try to get category component
                        component = get_nested_dict_value(code, 'productCategoryComponent.value', '')
                        if component:
                            if component == 'BRICK':
                                extracted_data['category'] = gpc_code
                            elif component == 'SEGMENT':
                                extracted_data['subcategory'] = gpc_code
    
    except Exception as e:
        logger.error(f"Error extracting product data: {e}")
    
    return extracted_data


def extract_search_results(search_results: Dict) -> Dict:
    """
    Extract structured data from search results
    
    Args:
        search_results (dict): Search results from the API
        
    Returns:
        dict: Structured search results with metadata and products
    """
    result = {
        'metadata': {
            'response_code': search_results.get('responseCode'),
            'response_message': search_results.get('responseMessage'),
            'total_results': int(search_results.get('totalNumOfResults', '0')),
            'next_cursor': search_results.get('nextCursorMark')
        },
        'products': []
    }
    
    # Extract product data
    for product in search_results.get('results', []):
        product_data = extract_product_data(product)
        result['products'].append(product_data)
    
    return result


def get_primary_image(product_data: Dict) -> str:
    """
    Get the primary image URL from product data
    
    Args:
        product_data (dict): Product data
        
    Returns:
        str: Primary image URL or empty string if not found
    """
    # First check if we already extracted the image URL
    if product_data.get('image_url'):
        return product_data['image_url']
    
    # Otherwise, look through images for a primary one
    for image in product_data.get('images', []):
        if image.get('is_primary'):
            return image.get('url', '')
    
    # If no primary image, return the first image if available
    if product_data.get('images'):
        return product_data['images'][0].get('url', '')
    
    return ''


def format_dimensions(dimensions: Dict) -> str:
    """
    Format dimensions as a string
    
    Args:
        dimensions (dict): Dimensions dictionary
        
    Returns:
        str: Formatted dimensions string
    """
    if not dimensions:
        return ''
    
    parts = []
    
    for dim_name in ['height', 'width', 'depth']:
        dim = dimensions.get(dim_name, {})
        if dim and dim.get('value') and dim.get('unit'):
            parts.append(f"{dim_name.capitalize()}: {dim['value']} {dim['unit']}")
    
    return ', '.join(parts)
