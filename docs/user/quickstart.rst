Quickstart
==========

This guide will help you get started with the 1WorldSync Content1 API Python Client.

Command Line Interface
--------------------

The package includes a command-line tool called ``ows`` that provides quick access to common operations:

.. code-block:: bash

   # Test your credentials
   ows login

   # Fetch products
   ows fetch --gtin 12345678901234
   ows fetch --target-market US --output results.json

   # Count products
   ows count
   ows count --target-market DE

   # Get product hierarchies
   ows hierarchy --gtin 12345678901234

For more details on the CLI, see :doc:`cli`.

Basic Setup
----------

First, import the client and initialize it with your credentials:

.. code-block:: python

   from oneworldsync import Content1Client
   import os
   from dotenv import load_dotenv
   
   # Load credentials from .env file
   load_dotenv()
   app_id = os.getenv("ONEWORLDSYNC_APP_ID")
   secret_key = os.getenv("ONEWORLDSYNC_SECRET_KEY")
   gln = os.getenv("ONEWORLDSYNC_USER_GLN")  # Optional
   
   # Initialize client
   client = Content1Client(app_id, secret_key, gln)

Counting Products
--------------

Count the number of products available:

.. code-block:: python

   # Count all products
   count = client.count_products()
   print(f"Total products: {count}")
   
   # Count products with criteria (traditional way)
   criteria = {
       "targetMarket": "US"
   }
   count = client.count_products(criteria)
   print(f"US products: {count}")
   
   # Count products with criteria builder (new way)
   from oneworldsync import ProductCriteria
   
   criteria = ProductCriteria().with_target_market("US")
   count = client.count_products(criteria)
   print(f"US products: {count}")

Fetching Products
-------------

Fetch products with various criteria:

.. code-block:: python

   # Fetch products by GTIN
   products = client.fetch_products_by_gtin(["00000000000000"])
   
   # Fetch products by Information Provider GLN
   products = client.fetch_products_by_ip_gln("1234567890123")
   
   # Fetch products by target market
   products = client.fetch_products_by_target_market("US")
   
   # New methods for common search patterns
   
   # Fetch products by date range
   products = client.fetch_products_by_date_range(
       from_date="2023-01-01", 
       to_date="2023-01-31",
       target_market="US"
   )
   
   # Fetch products from the last 30 days
   products = client.fetch_products_last_30_days(target_market="US")
   
   # Fetch products by brand name
   products = client.fetch_products_by_brand("Brand Name", target_market="US")
   
   # Fetch products by GPC code
   products = client.fetch_products_by_gpc_code("10000248", target_market="US")

Advanced Fetching
-----------------

Use more complex criteria for fetching products:

.. code-block:: python

   # Traditional way with dictionary
   criteria = {
       "targetMarket": "US",
       "fields": {
           "include": [
               "gtin", 
               "informationProviderGLN", 
               "targetMarket",
               "brandName", 
               "gpcCategory"
           ]
       },
       "sortFields": [
           {
               "field": "lastModifiedDate",
               "desc": True
           }
       ]
   }
   
   # Fetch products with page size
   products = client.fetch_products(criteria, page_size=100)
   
   # New way with criteria builder
   from oneworldsync import ProductCriteria, SortField
   
   criteria = ProductCriteria() \
       .with_target_market("US") \
       .with_fields(
           include=[
               "gtin", 
               "informationProviderGLN", 
               "targetMarket",
               "brandName", 
               "gpcCategory"
           ]
       ) \
       .with_sort([
           SortField.create("lastModifiedDate", descending=True)
       ])
   
   # Fetch products with page size
   products = client.fetch_products(criteria, page_size=100)

Working with Pagination
-------------------------

Handle pagination for large result sets:

.. code-block:: python

   # Fetch first page
   products = client.fetch_products(criteria, page_size=100)
   
   # Process first page - products is now a Content1ProductResults object
   for product in products:
       print(f"GTIN: {product.gtin}")
       print(f"Brand: {product.brand_name}")
   
   # Check if there are more pages
   if products.search_after:
       # Fetch next page using the simplified method
       next_page = client.fetch_next_page(products, page_size=100, original_criteria=criteria)
       
       # Process next page
       for product in next_page:
           print(f"GTIN: {product.gtin}")

Fetching Product Hierarchies
-------------------------

Get product hierarchy information:

.. code-block:: python

   # Fetch hierarchies
   hierarchies = client.fetch_hierarchies()
   
   # Process hierarchies - hierarchies is now a Content1HierarchyResults object
   for hierarchy in hierarchies:
       print(f"GTIN: {hierarchy.gtin}")
       print(f"Target Market: {hierarchy.target_market}")
       
       # Process hierarchy structure
       for level in hierarchy.hierarchy:
           print(f"Parent GTIN: {level.get('parentGtin')}")
           print(f"Child GTIN: {level.get('gtin')}")
           print(f"Quantity: {level.get('quantity')}")
   
   # You can also use the criteria builder for hierarchies
   from oneworldsync import ProductCriteria, DateRangeCriteria
   
   criteria = ProductCriteria() \
       .with_target_market("US") \
       .with_last_modified_date(DateRangeCriteria.last_30_days())
   
   hierarchies = client.fetch_hierarchies(criteria)

Error Handling
------------------------

Handle errors properly:

.. code-block:: python

   from oneworldsync import Content1Client, AuthenticationError, APIError
   
   try:
       products = client.fetch_products(criteria)
   except AuthenticationError as e:
       print(f"Authentication failed: {e}")
   except APIError as e:
       print(f"API error: {e}")
       print(f"Status code: {e.status_code}")
   except Exception as e:
       print(f"Unexpected error: {e}")