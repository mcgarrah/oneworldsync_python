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
   results = client.advanced_search("brandName", "Organic", rows=5)
   
   # Sort results
   results = client.advanced_search("productName", "Milk", sort="relevance")

Pagination
---------

When dealing with large result sets, you can use pagination:

.. code-block:: python

   # Get the first page of results
   results = client.free_text_search("milk", rows=10)
   
   # Get the next cursor from the results
   next_cursor = results.next_cursor
   
   # If there's a next cursor, get the next page
   if next_cursor:
       next_page = client.free_text_search("milk", rows=10, cursor=next_cursor)

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

Working with Product Data
-----------------------

The Product class provides convenient properties for accessing common product attributes:

.. code-block:: python

   # Get a product from search results
   product = results.products[0]
   
   # Access basic information
   print(f"ID: {product.item_id}")
   print(f"Brand: {product.brand_name}")
   print(f"Name: {product.product_name}")
   print(f"Description: {product.description}")
   
   # Access dimensions
   dimensions = product.dimensions
   if dimensions:
       print(f"Height: {dimensions['height']['value']} {dimensions['height']['unit']}")
       print(f"Width: {dimensions['width']['value']} {dimensions['width']['unit']}")
       print(f"Depth: {dimensions['depth']['value']} {dimensions['depth']['unit']}")
   
   # Access images
   for image in product.images:
       print(f"Image URL: {image['url']}")
       print(f"Is Primary: {image['is_primary']}")

You can also access the raw data directly:

.. code-block:: python

   # Access the raw data
   raw_data = product.data
   
   # Access specific fields in the raw data
   item = product.item