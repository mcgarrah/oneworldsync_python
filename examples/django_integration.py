#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Django integration example for the 1WorldSync Content1 API client.
This file demonstrates how to create a Django service for integrating with 1WorldSync.
"""

# This would typically be in a services.py file in your Django app

import logging
from django.conf import settings
from django.core.cache import cache

from oneworldsync import Content1Client, AuthenticationError, APIError

logger = logging.getLogger(__name__)

class OneWorldSyncService:
    """
    Service for interacting with the 1WorldSync Content1 API in a Django application.
    """
    
    def __init__(self):
        """Initialize the service with credentials from Django settings."""
        self.app_id = getattr(settings, 'ONEWORLDSYNC_APP_ID', None)
        self.secret_key = getattr(settings, 'ONEWORLDSYNC_SECRET_KEY', None)
        self.gln = getattr(settings, 'ONEWORLDSYNC_USER_GLN', None)
        self.api_url = getattr(settings, 'ONEWORLDSYNC_CONTENT1_API_URL', None)
        
        if not self.app_id or not self.secret_key:
            logger.warning("1WorldSync API credentials not configured")
            self.client = None
        else:
            # Initialize the client
            self.client = Content1Client(
                app_id=self.app_id,
                secret_key=self.secret_key,
                gln=self.gln,
                api_url=self.api_url
            )
    
    def get_product_by_gtin(self, gtin):
        """
        Fetch product data by GTIN using the Content1 API.
        
        Args:
            gtin (str): Global Trade Item Number
            
        Returns:
            dict: Product data or None if not found
        """
        if not self.client:
            logger.error("1WorldSync client not initialized")
            return None
        
        try:
            # Check cache first
            cache_key = f"1ws_product_{gtin}"
            cached_product = cache.get(cache_key)
            if cached_product:
                return cached_product
            
            # Use the Content1 API to fetch product data
            response = self.client.fetch_products_by_gtin([gtin])
            
            if response and 'items' in response and response['items']:
                product_data = response['items'][0]
                
                # Cache the result for 24 hours
                cache.set(cache_key, product_data, 86400)
                
                return product_data
            return None
        
        except Exception as e:
            logger.exception(f"Error fetching product {gtin} from 1WorldSync: {str(e)}")
            return None
    
    def search_products(self, criteria=None, page_size=10):
        """
        Search for products using the Content1 API.
        
        Args:
            criteria (dict, optional): Search criteria. Defaults to None.
            page_size (int, optional): Number of products to return. Defaults to 10.
            
        Returns:
            dict: Search results or None if error
        """
        if not self.client:
            logger.error("1WorldSync client not initialized")
            return None
        
        if criteria is None:
            criteria = {}
        
        try:
            # Use the Content1 API to fetch products
            response = self.client.fetch_products(criteria, page_size=page_size)
            
            return response
        
        except Exception as e:
            logger.exception(f"Error searching products from 1WorldSync: {str(e)}")
            return None
    
    def fetch_nutritional_products(self, segment_code=None, page_size=10):
        """
        Fetch food/beverage products with nutritional information.
        
        Args:
            segment_code (str, optional): GPC segment code. Defaults to None.
            page_size (int, optional): Number of products to return. Defaults to 10.
            
        Returns:
            list: List of products with nutritional information
        """
        if not self.client:
            logger.error("1WorldSync client not initialized")
            return []
        
        try:
            # Create criteria for food/beverage products
            criteria = {
                "targetMarket": "US",  # Focus on US market
                "fields": {
                    "include": [
                        "gtin",
                        "informationProviderGLN",
                        "targetMarket",
                        "lastModifiedDate",
                        "brandName",
                        "gpcCategory"
                    ]
                }
            }
            
            # Add segment code if provided
            if segment_code:
                criteria["gpcSegmentCode"] = segment_code
            
            # Fetch products
            response = self.client.fetch_products(criteria, page_size=page_size)
            
            if not response or 'items' not in response or not response['items']:
                logger.info("No products found")
                return []
            
            return response['items']
        
        except Exception as e:
            logger.exception(f"Error fetching nutritional products: {str(e)}")
            return []

# Example Django view that uses the service
"""
from django.shortcuts import render
from django.http import JsonResponse
from .services import OneWorldSyncService

def product_detail(request, gtin):
    # Initialize the service
    ows_service = OneWorldSyncService()
    
    # Get product data
    product_data = ows_service.get_product_by_gtin(gtin)
    
    if not product_data:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    # Return the product data
    return JsonResponse(product_data)

def search_products(request):
    # Initialize the service
    ows_service = OneWorldSyncService()
    
    # Get search parameters from request
    query = request.GET.get('q', '')
    target_market = request.GET.get('market', 'US')
    
    # Create search criteria
    criteria = {
        "targetMarket": target_market
    }
    
    if query:
        criteria["brandName"] = query
    
    # Search products
    results = ows_service.search_products(criteria)
    
    if not results:
        return JsonResponse({'products': []})
    
    # Return the search results
    return JsonResponse(results)

def nutritional_products(request):
    # Initialize the service
    ows_service = OneWorldSyncService()
    
    # Get segment code from request
    segment_code = request.GET.get('segment', '50030000')  # Default to Shelf Stable Food
    
    # Fetch nutritional products
    products = ows_service.fetch_nutritional_products(segment_code)
    
    # Return the products
    return JsonResponse({'products': products})
"""