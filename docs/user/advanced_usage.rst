Advanced Usage
=============

This guide covers advanced usage of the 1WorldSync Content1 API Python Client.

Date Range Queries
----------------

Create date range criteria for filtering products:

.. code-block:: python

   import datetime
   
   # Get current date and 30 days ago
   today = datetime.datetime.now()
   thirty_days_ago = today - datetime.timedelta(days=30)
   
   # Create date range criteria
   date_criteria = {
       "lastModifiedDate": {
           "from": {
               "date": thirty_days_ago.strftime("%Y-%m-%d"),
               "op": "GTE"
           },
           "to": {
               "date": today.strftime("%Y-%m-%d"),
               "op": "LTE"
           }
       }
   }
   
   # Use in a query
   products = client.fetch_products(date_criteria)

Field Selection
-------------

Select specific fields to include in the response:

.. code-block:: python

   # Create criteria with field selection
   criteria = {
       "fields": {
           "include": [
               "gtin",
               "informationProviderGLN",
               "targetMarket",
               "lastModifiedDate",
               "brandName",
               "gpcCategory"
           ]
       }
   }
   
   # Fetch products with selected fields
   products = client.fetch_products(criteria)

Sorting Results
------------

Sort results by one or more fields:

.. code-block:: python

   # Create criteria with sorting
   criteria = {
       "sortFields": [
           {
               "field": "lastModifiedDate",
               "desc": True  # Descending order
           },
           {
               "field": "gtin",
               "desc": False  # Ascending order
           }
       ]
   }
   
   # Fetch sorted products
   products = client.fetch_products(criteria)

Combining Multiple Criteria
------------------------

Combine multiple criteria for complex queries:

.. code-block:: python

   # Create combined criteria
   criteria = {
       # Target market
       "targetMarket": "US",
       
       # Date range
       "lastModifiedDate": date_criteria["lastModifiedDate"],
       
       # Field selection
       "fields": {
           "include": [
               "gtin",
               "informationProviderGLN",
               "targetMarket",
               "lastModifiedDate",
               "brandName",
               "gpcCategory"
           ]
       },
       
       # Sorting
       "sortFields": [
           {
               "field": "lastModifiedDate",
               "desc": True
           }
       ]
   }
   
   # Fetch products with combined criteria
   products = client.fetch_products(criteria)

Efficient Pagination
-----------------

Efficiently paginate through large result sets:

.. code-block:: python

   # Function to process all pages
   def process_all_pages(criteria, page_size=100):
       # Fetch first page
       current_page = client.fetch_products(criteria, page_size=page_size)
       
       # Process items from first page
       process_items(current_page.get("items", []))
       
       # Continue fetching pages until no more results
       while "searchAfter" in current_page:
           # Update criteria for next page
           next_criteria = criteria.copy()
           next_criteria["searchAfter"] = current_page["searchAfter"]
           
           # Fetch next page
           current_page = client.fetch_products(next_criteria, page_size=page_size)
           
           # Process items from current page
           process_items(current_page.get("items", []))
   
   # Function to process items
   def process_items(items):
       for item in items:
           # Process each item
           print(f"Processing GTIN: {item.get('gtin')}")
   
   # Use the function
   process_all_pages(criteria)

Working with Hierarchies
---------------------

Advanced usage with product hierarchies:

.. code-block:: python

   # Fetch hierarchies with criteria
   hierarchy_criteria = {
       "targetMarket": "US",
       "lastModifiedDate": date_criteria["lastModifiedDate"]
   }
   
   hierarchies = client.fetch_hierarchies(hierarchy_criteria)
   
   # Process hierarchies
   for hierarchy in hierarchies.get("hierarchies", []):
       print(f"Processing hierarchy for GTIN: {hierarchy.get('gtin')}")
       
       # Process hierarchy structure
       process_hierarchy_structure(hierarchy.get("hierarchy", []))
   
   # Function to recursively process hierarchy structure
   def process_hierarchy_structure(structure, level=0):
       for item in structure:
           indent = "  " * level
           print(f"{indent}Parent GTIN: {item.get('parentGtin')}")
           print(f"{indent}GTIN: {item.get('gtin')}")
           print(f"{indent}Quantity: {item.get('quantity')}")
           
           # Process children recursively
           if "children" in item and item["children"]:
               process_hierarchy_structure(item["children"], level + 1)

Saving Results to Files
--------------------

Save API responses to files for later processing:

.. code-block:: python

   import json
   
   # Fetch products
   products = client.fetch_products(criteria)
   
   # Save to file
   with open("products.json", "w") as f:
       json.dump(products, f, indent=2)
   
   # Fetch hierarchies
   hierarchies = client.fetch_hierarchies(hierarchy_criteria)
   
   # Save to file
   with open("hierarchies.json", "w") as f:
       json.dump(hierarchies, f, indent=2)