Advanced Usage
=============

This guide covers advanced usage patterns for the 1WorldSync Content1 API Python Client.

Using the Criteria Builder
------------------------

The library provides a fluent interface for building search criteria:

.. code-block:: python

   from oneworldsync import ProductCriteria, DateRangeCriteria, SortField
   
   # Create criteria using the builder pattern
   criteria = ProductCriteria() \
       .with_target_market("US") \
       .with_last_modified_date(DateRangeCriteria.last_30_days()) \
       .with_brand_name("Brand Name") \
       .with_sort([
           SortField.create("lastModifiedDate", descending=True)
       ])
   
   # Use the criteria with the client
   products = client.fetch_products(criteria)

Date Range Filtering
------------------

Filter products by date range:

.. code-block:: python

   # Get products modified in the last 30 days
   products = client.fetch_products_last_30_days(target_market="US")
   
   # Get products modified in a specific date range
   products = client.fetch_products_by_date_range(
       from_date="2023-01-01", 
       to_date="2023-01-31",
       target_market="US"
   )
   
   # Create a custom date range
   date_range = DateRangeCriteria.between("2023-01-01", "2023-01-31")
   criteria = ProductCriteria().with_last_modified_date(date_range)
   products = client.fetch_products(criteria)

Working with Product Results
-------------------------

The fetch methods now return structured objects:

.. code-block:: python

   # Fetch products
   results = client.fetch_products_by_brand("Brand Name")
   
   # Get the number of products
   print(f"Found {len(results)} products")
   
   # Iterate through products
   for product in results:
       print(f"GTIN: {product.gtin}")
       print(f"Brand: {product.brand_name}")
       print(f"Last Modified: {product.last_modified_date}")
   
   # Access the search_after token for pagination
   if results.search_after:
       next_page = client.fetch_next_page(results)

Advanced Filtering
---------------

Combine multiple criteria for complex searches:

.. code-block:: python

   criteria = ProductCriteria() \
       .with_target_market("US") \
       .with_gpc_code("10000248") \
       .with_brand_name("Brand Name") \
       .with_consumer_unit(True) \
       .with_product_type("EA")
   
   products = client.fetch_products(criteria)

Sorting Results
------------

Sort results by one or more fields:

.. code-block:: python

   criteria = ProductCriteria() \
       .with_target_market("US") \
       .with_sort([
           SortField.create("lastModifiedDate", descending=True),
           SortField.create("gtin", descending=False)
       ])
   
   products = client.fetch_products(criteria)

Field Selection
------------

Include or exclude specific fields in the response:

.. code-block:: python

   criteria = ProductCriteria() \
       .with_target_market("US") \
       .with_fields(
           include=[
               "gtin",
               "informationProviderGLN",
               "targetMarket",
               "lastModifiedDate",
               "brandName",
               "gpcCategory"
           ]
       )
   
   products = client.fetch_products(criteria)