Nutritional Data Integration
========================

Overview
--------

The 1WorldSync Content1 API provides access to product data including nutritional information for food and beverage products. This guide demonstrates how to extract and use nutritional information from the API.

Nutritional Data Structure
-------------------------

Our testing revealed that nutritional information in the Content1 API is found in:

.. code-block:: text

    item -> nutrientInformation -> nutrientDetail

Each nutrient detail contains:

- ``nutrientTypeCode``: The type of nutrient (e.g., "ENER-" for calories)
- ``quantityContained``: The amount of the nutrient
- ``dailyValueIntakePercent``: The percentage of daily value (if applicable)

Nutrient Code Mapping
--------------------

The Content1 API uses specific codes for nutrients that need to be mapped to more readable names:

+-------------+-------------------+------------------------+
| Nutrient Code | Description     | Example Field Name     |
+=============+===================+========================+
| ENER-       | Calories          | calories               |
+-------------+-------------------+------------------------+
| FATNLEA     | Total Fat         | total_fat_g            |
+-------------+-------------------+------------------------+
| FAT         | Total Fat         | total_fat_g            |
+-------------+-------------------+------------------------+
| FASAT       | Saturated Fat     | saturated_fat_g        |
+-------------+-------------------+------------------------+
| FATRN       | Trans Fat         | trans_fat_g            |
+-------------+-------------------+------------------------+
| CHOL-       | Cholesterol       | cholesterol_mg         |
+-------------+-------------------+------------------------+
| NA          | Sodium            | sodium_mg              |
+-------------+-------------------+------------------------+
| CHO-        | Total Carbohydrate| total_carbohydrate_g   |
+-------------+-------------------+------------------------+
| FIBTSW      | Dietary Fiber     | dietary_fiber_g        |
+-------------+-------------------+------------------------+
| SUGAR-      | Total Sugars      | total_sugars_g         |
+-------------+-------------------+------------------------+
| PRO-        | Protein           | protein_g              |
+-------------+-------------------+------------------------+

Known Food Product GTINs
-----------------------

We've identified several GTINs that reliably contain nutritional information:

- ``00037600168526``: Hormel Chorizo
- ``00028400083140``: Doritos
- ``00018000428434``: Cheerios
- ``00044000026882``: Pepsi
- ``00079100851744``: Ritz Crackers

Example: Extracting Nutritional Information
------------------------------------------

.. code-block:: python

    from oneworldsync import Content1Client

    # Initialize client
    client = Content1Client(
        app_id='your_app_id',
        secret_key='your_secret_key'
    )

    # Fetch a product with nutritional information
    gtin = "00037600168526"  # Hormel Chorizo
    response = client.fetch_products_by_gtin([gtin])
    
    if response and 'items' in response and response['items']:
        product = response['items'][0]
        item = product.get('item', {})
        
        # Extract nutritional information
        nutrient_info = item.get('nutrientInformation', [])
        
        for info in nutrient_info:
            # Extract serving size
            serving_size = info.get('servingSize', [])
            if serving_size and len(serving_size) > 0:
                value = serving_size[0].get('value', '')
                unit = serving_size[0].get('qual', '')
                print(f"Serving Size: {value} {unit}")
            
            # Extract nutrient details
            nutrient_details = info.get('nutrientDetail', [])
            
            for nutrient in nutrient_details:
                nutrient_type = nutrient.get('nutrientTypeCode', '')
                
                # Get quantity
                quantity = nutrient.get('quantityContained', [])
                value = quantity[0].get('value', '') if quantity else ''
                unit = quantity[0].get('qual', '') if quantity else ''
                
                # Get daily value percentage
                daily_value = nutrient.get('dailyValueIntakePercent', '')
                dv_str = f" ({daily_value}% DV)" if daily_value else ""
                
                print(f"{nutrient_type}: {value} {unit}{dv_str}")

For more detailed examples, see the ``examples`` directory in the repository.

Limitations
----------

- Not all products have complete nutritional information
- The structure of the data can vary between products
- Some nutrient codes may not be standardized across all products
- The GTIN field may not be populated in the API response