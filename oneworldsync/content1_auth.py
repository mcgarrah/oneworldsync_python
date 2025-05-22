"""
Authentication module for 1WorldSync Content1 API

This module provides authentication mechanisms for the 1WorldSync Content1 API,
including HMAC authentication as required by the API.
"""

import base64
import hashlib
import hmac
import urllib.parse
from datetime import datetime, timezone


class Content1HMACAuth:
    """
    HMAC Authentication for 1WorldSync Content1 API
    
    This class handles the HMAC authentication process required by the 1WorldSync Content1 API.
    It generates the necessary hash code based on the request parameters and secret key.
    """
    
    def __init__(self, app_id, secret_key, gln=None):
        """
        Initialize the HMAC authentication with app_id and secret_key
        
        Args:
            app_id (str): The application ID provided by 1WorldSync
            secret_key (str): The secret key provided by 1WorldSync
            gln (str, optional): Global Location Number for the user
        """
        self.app_id = app_id
        self.secret_key = secret_key
        self.gln = gln
    
    def generate_timestamp(self):
        """
        Generate a timestamp in the format required by the 1WorldSync Content1 API
        
        Returns:
            str: Timestamp in ISO 8601 format (YYYY-MM-DDThh:mm:ssZ)
        """
        return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def generate_hash(self, uri):
        """
        Generate a hash code for the given URI using HMAC-SHA256
        
        Args:
            uri (str): The URI to hash
            
        Returns:
            str: Base64-encoded hash code
        """
        # URL-encode the URI before hashing - use encodeURIComponent equivalent
        # This is critical to match the TypeScript implementation
        encoded_uri = urllib.parse.quote(uri, safe='')
        
        # Print debug info
        print(f"Original URI: {uri}")
        print(f"Encoded URI: {encoded_uri}")
        print(f"Secret key: {self.secret_key}")
        
        # Create an HMAC using SHA256 and the secret key
        hash_obj = hmac.new(
            bytes(self.secret_key, 'utf-8'),
            bytes(encoded_uri, 'utf-8'),
            hashlib.sha256
        )
        
        # Get the hash and print it
        hash_result = base64.b64encode(hash_obj.digest()).decode('utf-8')
        print(f"Generated hash: {hash_result}")
        
        # Return the Base64-encoded hash
        return hash_result
    
    def generate_auth_headers(self, uri):
        """
        Generate authentication headers for a request
        
        Args:
            uri (str): The URI part of the URL (path + query parameters)
            
        Returns:
            dict: Headers containing authentication information
        """
        # Generate the hash code
        hash_code = self.generate_hash(uri)
        
        # Create headers
        headers = {
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'appid': self.app_id,
            'hashcode': hash_code
        }
        
        # Add GLN if provided
        if self.gln:
            headers['gln'] = self.gln
        
        return headers