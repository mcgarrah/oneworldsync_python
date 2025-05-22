Authentication
==============

This guide explains how to authenticate with the 1WorldSync Content1 API.

Authentication Credentials
-----------------------

To use the 1WorldSync Content1 API, you need the following credentials:

1. **App ID**: Your application identifier provided by 1WorldSync
2. **Secret Key**: Your secret key provided by 1WorldSync
3. **GLN** (optional): Global Location Number for the user

Setting Up Authentication
----------------------

There are two ways to set up authentication:

1. **Direct initialization**:

   .. code-block:: python

      from oneworldsync import Content1Client
      
      client = Content1Client(
          app_id='your_app_id',
          secret_key='your_secret_key',
          gln='your_gln'  # Optional
      )

2. **Environment variables**:

   Set the following environment variables:

   .. code-block:: bash

      ONEWORLDSYNC_APP_ID=your_app_id
      ONEWORLDSYNC_SECRET_KEY=your_secret_key
      ONEWORLDSYNC_USER_GLN=your_gln  # Optional
      ONEWORLDSYNC_CONTENT1_API_URL=https://content1-api.1worldsync.com  # Optional

   Then initialize the client without parameters:

   .. code-block:: python

      from oneworldsync import Content1Client
      
      client = Content1Client()

Using a .env File
--------------

For development, you can use a `.env` file to store your credentials:

1. Create a `.env` file in your project directory:

   .. code-block:: bash

      ONEWORLDSYNC_APP_ID=your_app_id
      ONEWORLDSYNC_SECRET_KEY=your_secret_key
      ONEWORLDSYNC_USER_GLN=your_gln
      ONEWORLDSYNC_CONTENT1_API_URL=https://content1-api.1worldsync.com

2. Load the environment variables using the `python-dotenv` package:

   .. code-block:: python

      import os
      from dotenv import load_dotenv
      from oneworldsync import Content1Client
      
      # Load environment variables from .env file
      load_dotenv()
      
      # Initialize client using environment variables
      client = Content1Client()

Authentication Process
------------------

The 1WorldSync Content1 API uses HMAC authentication. The client handles this process automatically:

1. The client generates a timestamp for the request
2. The client constructs the URI with the timestamp
3. The client generates a hash code using the secret key and URI
4. The client adds the app ID, hash code, and GLN (if provided) to the request headers

For more details on the HMAC authentication process, refer to the 1WorldSync Content1 API HMAC Guide.