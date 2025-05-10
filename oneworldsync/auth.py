"""
Authentication module for 1WorldSync API

This module provides authentication mechanisms for the 1WorldSync API,
including HMAC authentication as required by the API.
"""

import hashlib
import hmac
import base64
import urllib.parse
import datetime


class HMACAuth:
    """
    HMAC Authentication for 1WorldSync API
    
    This class handles the HMAC authentication process required by the 1WorldSync API.
    It generates the necessary hash code based on the request parameters and secret key.
    """
    
    def __init__(self, app_id, secret_key):
        """
        Initialize the HMAC authentication with app_id and secret_key
        
        Args:
            app_id (str): The application ID provided by 1WorldSync
            secret_key (str): The secret key provided by 1WorldSync
        """
        self.app_id = app_id
        self.secret_key = secret_key
    
    def generate_timestamp(self):
        """
        Generate a timestamp in the format required by the 1WorldSync API
        
        Returns:
            str: Timestamp in ISO 8601 format (YYYY-MM-DDThh:mm:ssZ)
        """
        return datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def generate_hash(self, string_to_hash):
        """
        Generate a hash code for the given string using HMAC-SHA256
        
        Args:
            string_to_hash (str): The string to hash
            
        Returns:
            str: Base64-encoded hash code
        """
        message = bytes(string_to_hash, 'utf-8')
        secret = bytes(self.secret_key, 'utf-8')
        hash_obj = hmac.new(secret, message, hashlib.sha256)
        return base64.b64encode(hash_obj.digest()).decode('utf-8')
    
    def prepare_auth_params(self, path, query_params):
        """
        Prepare authentication parameters for a request
        
        Args:
            path (str): API endpoint path
            query_params (dict): Query parameters for the request
            
        Returns:
            dict: Updated query parameters with authentication information
        """
        # Create a copy of the query parameters to avoid modifying the original
        params = query_params.copy()
        
        # Add required authentication parameters
        params['app_id'] = self.app_id
        
        # Add timestamp if not already present
        if 'TIMESTAMP' not in params:
            params['TIMESTAMP'] = self.generate_timestamp()
        
        # Create the string to hash
        param_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
        string_to_hash = f"/{path}?{param_string}"
        
        # Generate hash code
        hash_code = self.generate_hash(string_to_hash)
        
        # Add hash code to parameters
        params['hash_code'] = hash_code
        
        return params
    
    def get_auth_url(self, protocol, domain, path, query_params):
        """
        Get a fully authenticated URL for the 1WorldSync API
        
        Args:
            protocol (str): URL protocol (http:// or https://)
            domain (str): API domain
            path (str): API endpoint path
            query_params (dict): Query parameters for the request
            
        Returns:
            str: Fully authenticated URL
        """
        # Prepare authentication parameters
        auth_params = self.prepare_auth_params(path, query_params)
        
        # URL encode parameters
        encoded_params = []
        for key, value in auth_params.items():
            encoded_key = urllib.parse.quote(str(key))
            encoded_value = urllib.parse.quote(str(value))
            encoded_params.append(f"{encoded_key}={encoded_value}")
        
        # Construct URL
        query_string = '&'.join(encoded_params)
        return f"{protocol}{domain}/{path}?{query_string}"