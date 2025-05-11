Error Handling
=============

The OneWorldSync Python Client provides custom exceptions for handling different types of errors.

Exception Hierarchy
-----------------

- ``OneWorldSyncError``: Base exception for all errors
  - ``AuthenticationError``: Raised when authentication fails
  - ``APIError``: Raised when the API returns an error response

Basic Error Handling
------------------

Here's a basic example of error handling:

.. code-block:: python

   from oneworldsync import OneWorldSyncClient, AuthenticationError, APIError
   
   try:
       client = OneWorldSyncClient(app_id, secret_key)
       results = client.free_text_search("apple")
   except AuthenticationError as e:
       print(f"Authentication failed: {e}")
   except APIError as e:
       print(f"API error: {e}")
       print(f"Status code: {e.status_code}")
   except Exception as e:
       print(f"Unexpected error: {e}")

Authentication Errors
-------------------

Authentication errors occur when the API rejects your credentials:

.. code-block:: python

   try:
       client = OneWorldSyncClient(app_id, secret_key)
       results = client.free_text_search("apple")
   except AuthenticationError as e:
       print(f"Authentication failed: {e}")
       # Handle authentication error (e.g., prompt for new credentials)

Common causes of authentication errors:

1. Incorrect App ID or Secret Key
2. Using credentials for the wrong environment (production vs. preprod)
3. System clock not synchronized (timestamp accuracy is important)

API Errors
---------

API errors occur when the API returns an error response:

.. code-block:: python

   try:
       client = OneWorldSyncClient(app_id, secret_key)
       results = client.free_text_search("apple")
   except APIError as e:
       print(f"API error: {e}")
       print(f"Status code: {e.status_code}")
       
       # Access the full response if available
       if e.response:
           print(f"Response: {e.response}")
       
       # Handle specific status codes
       if e.status_code == 400:
           print("Bad request - check your parameters")
       elif e.status_code == 404:
           print("Resource not found")
       elif e.status_code == 429:
           print("Rate limit exceeded - try again later")
       elif e.status_code >= 500:
           print("Server error - try again later")

Network Errors
------------

Network errors can occur when there are connectivity issues:

.. code-block:: python

   import requests
   
   try:
       client = OneWorldSyncClient(app_id, secret_key)
       results = client.free_text_search("apple")
   except requests.exceptions.ConnectionError:
       print("Connection error - check your internet connection")
   except requests.exceptions.Timeout:
       print("Request timed out - try again later")
   except requests.exceptions.RequestException as e:
       print(f"Network error: {e}")

Best Practices
------------

1. **Always handle exceptions**: Wrap API calls in try-except blocks
2. **Log errors**: Log detailed error information for debugging
3. **Implement retries**: For transient errors (e.g., network issues, rate limiting)
4. **Provide user feedback**: Display meaningful error messages to users
5. **Check status codes**: Handle different status codes appropriately