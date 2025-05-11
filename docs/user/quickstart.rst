Quickstart
==========

This guide will help you get started with the OneWorldSync Python Client.

Basic Setup
----------

First, import the client and initialize it with your credentials:

.. code-block:: python

   from oneworldsync import OneWorldSyncClient
   import os
   from dotenv import load_dotenv
   
   # Load credentials from .env file
   load_dotenv()
   app_id = os.getenv("ONEWORLDSYNC_APP_ID")
   secret_key = os.getenv("ONEWORLDSYNC_SECRET_KEY")
   
   # Initialize client
   client = OneWorldSyncClient(app_id, secret_key)

Free Text Search
--------------

Perform a simple free text search:

.. code-block:: python

   # Search for products containing "milk"
   results = client.free_text_search("milk")
   
   # Print number of results
   print(f"Found {len(results.products)} products")
   
   # Print details of the first product
   if results.products:
       product = results.products[0]
       print(f"Product: {product.brand_name} - {product.product_name}")
       print(f"Description: {product.description}")

Advanced Search
-------------

Search for a product by a specific field:

.. code-block:: python

   # Search for a product by UPC
   results = client.advanced_search("itemIdentifier", "16241419122223")
   
   # Search for products by brand
   results = client.advanced_search("brandName", "Organic Valley")

Geo-Location Search
-----------------

Search for products with geo-location context:

.. code-block:: python

   # Search with geo location (San Francisco coordinates)
   results = client.free_text_search(
       "coffee",
       geo_location=(37.7749, -122.4194)
   )

Working with Search Results
-------------------------

Iterate through search results:

.. code-block:: python

   # Iterate through products
   for product in results.products:
       print(f"ID: {product.item_id}")
       print(f"Brand: {product.brand_name}")
       print(f"Name: {product.product_name}")
       print(f"Description: {product.description}")
       
       # Get product dimensions
       dimensions = product.dimensions
       if dimensions:
           print(f"Dimensions: {dimensions['height']['value']} {dimensions['height']['unit']} x "
                 f"{dimensions['width']['value']} {dimensions['width']['unit']} x "
                 f"{dimensions['depth']['value']} {dimensions['depth']['unit']}")
       
       # Get product images
       for image in product.images:
           print(f"Image URL: {image['url']} (Primary: {image['is_primary']})")

Fetching a Specific Product
-------------------------

Get a specific product by ID:

.. code-block:: python

   # Get a product by ID
   product_data = client.get_product("some_product_id")
   
   # Process the product data
   # Note: This returns the raw API response, not a Product object