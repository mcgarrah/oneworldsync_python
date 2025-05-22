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
        # According to the error "Hashcode mismatch", we need to ensure our hash matches
        # what the server expects. Let's try without URL encoding the URI.
        
        # Create an HMAC using SHA256 and the secret key
        hash_obj = hmac.new(
            bytes(self.secret_key, 'utf-8'),
            bytes(uri, 'utf-8'),
            hashlib.sha256
        )
        
        # Return the Base64-encoded hash
        return base64.b64encode(hash_obj.digest()).decode('utf-8')
    
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
        
        # Debug information
        # print(f"DEBUG - URI for hash generation: {uri}")
        # print(f"DEBUG - Generated hash code: {hash_code}")
        
        # Create headers
        headers = {
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'appId': self.app_id,  # Changed from 'appid' to 'appId' to match API requirements
            'hashCode': hash_code  # Changed from 'hashcode' to 'hashCode' to match API requirements
        }
        
        # Add GLN if provided
        if self.gln:
            headers['gln'] = self.gln
        
        # Debug information
        # print(f"DEBUG - Generated headers: {headers}")
        
        return headers