Advanced Usage
=============

This guide covers advanced usage of the OneWorldSync Python Client.

Advanced Search Options
---------------------

The advanced search functionality allows you to search for products using specific fields:

.. code-block:: python

   # Search by GTIN
   results = client.advanced_search("gtin", "12345678901234")
   
   # Search by brand name
   results = client.advanced_search("brandName", "Organic Valley")
   
   # Search by product name
   results = client.advanced_search("productName", "Whole Milk")

You can also add additional parameters to refine your search:

.. code-block:: python

   # Limit the number of results
   results = client.advanced_search("brandName", "Organic", limit=5)
   
   # Sort results
   results = client.advanced_search("productName", "Milk", sort="relevance")

Pagination
---------

When dealing with large result sets, you can use pagination:

.. code-block:: python

   # Get the first page of results
   results = client.free_text_search("milk", limit=10)
   
   # Get the next cursor from the results
   next_cursor = results.next_cursor
   
   # If there's a next cursor, get the next page
   if next_cursor:
       next_page = client.free_text_search("milk", limit=10, cursor=next_cursor)

Geo-Location Search
-----------------

You can include geo-location information in your searches:

.. code-block:: python

   # Search with geo-location (latitude, longitude)
   results = client.free_text_search(
       "coffee",
       geo_location=(37.7749, -122.4194)  # San Francisco coordinates
   )

Custom API URL
------------

If you need to use a different API URL (e.g., for testing or preprod):

.. code-block:: python

   # Use a custom API URL
   client = OneWorldSyncClient(
       app_id="your_app_id",
       secret_key="your_secret_key",
       api_url="preprod.api.1worldsync.com"
   )

Request Timeout
-------------

You can customize the request timeout:

.. code-block:: python

   # Set a custom timeout (in seconds)
   client = OneWorldSyncClient(
       app_id="your_app_id",
       secret_key="your_secret_key",
       timeout=60  # 60 seconds
   )

Enhanced Product Data Access
--------------------------

The Product class provides enhanced properties for easier access to product data:

.. code-block:: python

   # Get a product from search results
   product = results.products[0]
   
   # Access basic information
   print(f"ID: {product.item_id}")
   print(f"GTIN: {product.gtin}")
   print(f"Brand: {product.brand_name}")
   print(f"Name: {product.product_name}")
   print(f"Description: {product.description}")
   
   # Access primary image URL directly
   print(f"Primary Image: {product.primary_image_url}")
   
   # Get formatted dimensions as a string
   print(f"Dimensions: {product.formatted_dimensions}")
   
   # Access additional product information
   print(f"GPC Code: {product.gpc_code}")
   print(f"Category: {product.category}")
   print(f"Country of Origin: {product.country_of_origin}")
   print(f"Ingredients: {product.ingredients}")
   
   # Access all images
   for image in product.images:
       print(f"Image URL: {image['url']}")
       print(f"Is Primary: {image['is_primary']}")

Converting to Dictionaries
------------------------

You can convert products and search results to clean dictionaries:

.. code-block:: python

   # Convert a product to a dictionary
   product_dict = product.to_dict()
   
   # Convert entire search results to a dictionary
   results_dict = results.to_dict()
   
   # Access metadata from the dictionary
   metadata = results_dict['metadata']
   print(f"Total results: {metadata['total_results']}")
   
   # Access products from the dictionary
   products = results_dict['products']
   for p in products:
       print(f"{p['brand_name']} - {p['product_name']}")

Raw Data Access
------------

You can still access the raw data directly if needed:

.. code-block:: python

   # Access the raw data
   raw_data = product.data
   
   # Access specific fields in the raw data
   item = product.item