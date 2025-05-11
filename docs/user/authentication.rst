Authentication
=============

The 1WorldSync API uses HMAC authentication. You'll need an App ID and Secret Key from 1WorldSync to authenticate your requests.

Obtaining Credentials
-------------------

To obtain credentials for the 1WorldSync API:

1. Contact 1WorldSync to request API access
2. You will receive an App ID and Secret Key
3. These credentials are specific to either the production or preprod environment

Storing Credentials
-----------------

You can store your credentials in a ``.env`` file:

.. code-block:: ini

   ONEWORLDSYNC_APP_ID=your_app_id
   ONEWORLDSYNC_SECRET_KEY=your_secret_key
   ONEWORLDSYNC_API_URL=1ws_api_endpoint

Then load them in your code:

.. code-block:: python

   import os
   from dotenv import load_dotenv
   
   # Load credentials from .env file
   load_dotenv()
   app_id = os.getenv("ONEWORLDSYNC_APP_ID")
   secret_key = os.getenv("ONEWORLDSYNC_SECRET_KEY")

Authentication Process
--------------------

The 1WorldSync API requires a specific HMAC authentication process:

1. The client constructs a string containing the request parameters in a specific order
2. The string is hashed using HMAC-SHA256 with the secret key
3. The hash is base64-encoded and included in the request as the ``hash_code`` parameter

**Important Note**: The 1WorldSync API is very particular about the order of parameters in the authentication process. The parameters must be in a specific order when constructing the string to hash. This library handles this complexity for you, ensuring that parameters are ordered correctly for authentication.

Using the Client
--------------

The OneWorldSyncClient handles authentication automatically:

.. code-block:: python

   from oneworldsync import OneWorldSyncClient
   
   # Initialize client with credentials
   client = OneWorldSyncClient(app_id, secret_key)
   
   # All API calls will be automatically authenticated
   results = client.free_text_search("milk")

Authentication Errors
-------------------

If authentication fails, an ``AuthenticationError`` will be raised:

.. code-block:: python

   from oneworldsync import OneWorldSyncClient, AuthenticationError
   
   try:
       client = OneWorldSyncClient(app_id, secret_key)
       results = client.free_text_search("milk")
   except AuthenticationError as e:
       print(f"Authentication failed: {e}")

Common authentication issues include:

1. Incorrect App ID or Secret Key
2. Using credentials for the wrong environment (production vs. preprod)
3. System clock not synchronized (timestamp accuracy is important for authentication)