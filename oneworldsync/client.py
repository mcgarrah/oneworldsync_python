"""
1WorldSync API Client

This module provides a client for interacting with the 1WorldSync API.
"""

import os
import requests
from .auth import HMACAuth
from .exceptions import APIError, AuthenticationError


class OneWorldSyncClient:
    """
    Client for the 1WorldSync API
    
    This class provides methods for interacting with the 1WorldSync API,
    handling authentication, request construction, and response parsing.
    """
    
    def __init__(self, app_id=None, secret_key=None, api_url=None, timeout=30):
        """
        Initialize the 1WorldSync API client
        
        Args:
            app_id (str, optional): The application ID provided by 1WorldSync. 
                                   If None, will try to get from ONEWORLDSYNC_APP_ID environment variable.
            secret_key (str, optional): The secret key provided by 1WorldSync.
                                       If None, will try to get from ONEWORLDSYNC_SECRET_KEY environment variable.
            api_url (str, optional): The API URL to use. 
                                    If None, will try to get from ONEWORLDSYNC_API_URL environment variable.
                                    Defaults to preprod API if not specified.
            timeout (int, optional): Request timeout in seconds. Defaults to 30.
        """
        # Get credentials from environment variables if not provided
        self.app_id = app_id or os.environ.get('ONEWORLDSYNC_APP_ID')
        self.secret_key = secret_key or os.environ.get('ONEWORLDSYNC_SECRET_KEY')
        
        if not self.app_id or not self.secret_key:
            raise ValueError("APP_ID and SECRET_KEY must be provided either as parameters or environment variables")
        
        self.auth = HMACAuth(self.app_id, self.secret_key)
        self.protocol = 'https://'
        
        # Get API URL from environment variable if not provided
        default_api_url = 'marketplace.preprod.api.1worldsync.com'
        if api_url:
            # If full URL is provided, extract just the domain
            if '://' in api_url:
                self.domain = api_url.split('://')[-1].split('/')[0]
            else:
                self.domain = api_url
        else:
            env_api_url = os.environ.get('ONEWORLDSYNC_API_URL')
            if env_api_url:
                # If full URL is provided in env var, extract just the domain
                if '://' in env_api_url:
                    self.domain = env_api_url.split('://')[-1].split('/')[0]
                else:
                    self.domain = env_api_url
            else:
                self.domain = default_api_url
        
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
    
    def search_products(self, query, search_type='freeTextSearch', access_mdm='computer', geo_location=None, **kwargs):
        """
        Search for products using the 1WorldSync API
        
        Args:
            query (str): Search query
            search_type (str, optional): Type of search ('freeTextSearch', 'advancedSearch', 'categoryCode'). Defaults to 'freeTextSearch'.
            access_mdm (str, optional): Access MDM. Defaults to 'computer'.
            geo_location (tuple, optional): Tuple of (latitude, longitude). Defaults to None.
            **kwargs: Additional search parameters
            
        Returns:
            dict: Search results
        """
        # Prepare parameters - use exact parameter names from the API documentation
        params = {
            'searchType': search_type,
            'query': query,
            'access_mdm': access_mdm,
        }
        
        # Debug the parameters
        print(f"DEBUG - Search parameters: {params}")
        
        # Add geo location if provided
        if geo_location:
            params['geo_loc_access_latd'] = geo_location[0]
            params['geo_loc_access_long'] = geo_location[1]
        
        # Add additional parameters
        params.update(kwargs)
        
        # Make request
        response = self._make_request('GET', 'V2/products', params)
        
        # Import here to avoid circular imports
        from .models import SearchResults
        return SearchResults(response)
    
    def get_product(self, product_id, access_mdm='computer', geo_location=None, **kwargs):
        """
        Get a product by ID from the search results. It is not a UPC/EAN/GTIN.
        itemReferenceId is the 1WorldSync assigned unique identifier for this product.
        
        Args:
            product_id (str): Product ID
            access_mdm (str, optional): Access MDM. Defaults to 'computer'.
            geo_location (tuple, optional): Tuple of (latitude, longitude). Defaults to None.
            **kwargs: Additional parameters
            
        Returns:
            dict: Product details
        """
        # Prepare parameters - use exact parameter names from the API documentation
        params = {
            'access_mdm': access_mdm,
        }
        
        # Debug the parameters
        print(f"DEBUG - Search parameters: {params}")
        
        # Add geo location if provided
        if geo_location:
            params['geo_loc_access_latd'] = geo_location[0]
            params['geo_loc_access_long'] = geo_location[1]
        
        # Add additional parameters
        params.update(kwargs)
        
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
        # Try different query formats for advanced search
        # Format 1: field:value (standard Lucene syntax)
        query = f"{field}:{value}"
        
        # Print debug info
        print(f"DEBUG - Advanced search query: {query}")
        
        try:
            return self.search_products(query, 'advancedSearch', access_mdm, **kwargs)
        except APIError as e:
            if e.status_code == 400:
                # If the standard format fails, try with quotes
                query = f"{field}:\"{value}\""
                print(f"DEBUG - Retrying with quoted value: {query}")
                try:
                    return self.search_products(query, 'advancedSearch', access_mdm, **kwargs)
                except APIError:
                    # If that fails too, try with a JSON-like format
                    query = f"\"{field}\":\"{value}\""
                    print(f"DEBUG - Retrying with JSON-like format: {query}")
                    return self.search_products(query, 'advancedSearch', access_mdm, **kwargs)
            else:
                # If it's not a 400 error, re-raise the original exception
                raise
    
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
        return self.search_products(query, 'freeTextSearch', access_mdm, **kwargs)
