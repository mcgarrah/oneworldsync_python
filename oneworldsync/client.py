"""
1WorldSync API Client

This module provides a client for interacting with the 1WorldSync API.
"""

import requests
import urllib.parse
from .auth import HMACAuth
from .exceptions import APIError, AuthenticationError


class OneWorldSyncClient:
    """
    Client for the 1WorldSync API
    
    This class provides methods for interacting with the 1WorldSync API,
    handling authentication, request construction, and response parsing.
    """
    
    def __init__(self, app_id, secret_key, use_production=False, timeout=30):
        """
        Initialize the 1WorldSync API client
        
        Args:
            app_id (str): The application ID provided by 1WorldSync
            secret_key (str): The secret key provided by 1WorldSync
            use_production (bool, optional): Whether to use the production API. Defaults to False.
            timeout (int, optional): Request timeout in seconds. Defaults to 30.
        """
        self.auth = HMACAuth(app_id, secret_key)
        self.protocol = 'https://'
        self.domain = 'marketplace.api.1worldsync.com' if use_production else 'marketplace.preprod.api.1worldsync.com'
        self.timeout = timeout
    
    def _make_request(self, method, path, params=None, data=None, headers=None):
        """
        Make a request to the 1WorldSync API
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            path (str): API endpoint path
            params (dict, optional): Query parameters. Defaults to None.
            data (dict, optional): Request body data. Defaults to None.
            headers (dict, optional): Request headers. Defaults to None.
            
        Returns:
            dict: API response parsed as JSON
            
        Raises:
            AuthenticationError: If authentication fails
            APIError: If the API returns an error
        """
        # Initialize parameters if None
        if params is None:
            params = {}
        
        # Get authenticated URL
        url = self.auth.get_auth_url(self.protocol, self.domain, path, params)
        
        # Set default headers if None
        if headers is None:
            headers = {'Content-Type': 'application/json'}
        
        # Make request
        try:
            response = requests.request(
                method,
                url,
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            
            # Check for errors
            if response.status_code == 401:
                raise AuthenticationError("Authentication failed")
            
            if response.status_code >= 400:
                raise APIError(
                    response.status_code,
                    response.text,
                    response
                )
            
            # Parse response
            return response.json()
        
        except requests.exceptions.RequestException as e:
            raise APIError(0, str(e))
    
    def search_products(self, search_type, query, access_mdm='computer', geo_location=None, **kwargs):
        """
        Search for products using the 1WorldSync API
        
        Args:
            search_type (str): Type of search ('freeTextSearch', 'advancedSearch', etc.)
            query (str): Search query
            access_mdm (str, optional): Access MDM. Defaults to 'computer'.
            geo_location (tuple, optional): Tuple of (latitude, longitude). Defaults to None.
            **kwargs: Additional search parameters
            
        Returns:
            dict: Search results
        """
        # Prepare parameters
        params = {
            'searchType': search_type,
            'query': query,
            'access_mdm': access_mdm,
        }
        
        # Add geo location if provided
        if geo_location:
            params['geo_loc_access_latd'] = geo_location[0]
            params['geo_loc_access_long'] = geo_location[1]
        
        # Add additional parameters
        params.update(kwargs)
        
        # Make request
        return self._make_request('GET', 'V2/products', params)
    
    def get_product(self, product_id, **kwargs):
        """
        Get a product by ID
        
        Args:
            product_id (str): Product ID
            **kwargs: Additional parameters
            
        Returns:
            dict: Product details
        """
        # Prepare parameters
        params = kwargs
        
        # Make request
        return self._make_request('GET', f'V2/products/{product_id}', params)
    
    def advanced_search(self, field, value, access_mdm='computer', **kwargs):
        """
        Perform an advanced search
        
        Args:
            field (str): Field to search in
            value (str): Value to search for
            access_mdm (str, optional): Access MDM. Defaults to 'computer'.
            **kwargs: Additional search parameters
            
        Returns:
            dict: Search results
        """
        query = f"{field}:{value}"
        return self.search_products('advancedSearch', query, access_mdm, **kwargs)
    
    def free_text_search(self, query, access_mdm='computer', **kwargs):
        """
        Perform a free text search
        
        Args:
            query (str): Search query
            access_mdm (str, optional): Access MDM. Defaults to 'computer'.
            **kwargs: Additional search parameters
            
        Returns:
            dict: Search results
        """
        return self.search_products('freeTextSearch', query, access_mdm, **kwargs)