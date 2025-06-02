# 1WorldSync Nutritional Data Integration

This guide explains how to use the 1WorldSync Content1 API to retrieve product data with nutritional information for Food/Beverage segments in a Django application.

## Overview

The 1WorldSync Content1 API provides access to product data including nutritional information for food and beverage products. This guide demonstrates how to:

1. Fetch food/beverage products using specific GTINs or GPC segment codes
2. Extract nutritional information from the API response
3. Map the data to Django models
4. Integrate with a Django application

## Example Files

- `simple_nutrition_example.py`: Simple standalone example showing how to fetch nutritional data
- `django_nutrition_service.py`: Django service for retrieving nutritional information
- `django_food_nutrition_example.py`: Example showing how to fetch and process nutritional data
- `django_views.py`: Example Django views that use the NutritionService

## Nutritional Data Structure

Our testing revealed that nutritional information in the Content1 API is found in:

```
item -> nutrientInformation -> nutrientDetail
```

Each nutrient detail contains:
- `nutrientTypeCode`: The type of nutrient (e.g., "ENER-" for calories)
- `quantityContained`: The amount of the nutrient
- `dailyValueIntakePercent`: The percentage of daily value (if applicable)

## Nutrient Code Mapping

The Content1 API uses specific codes for nutrients that need to be mapped to Django model fields:

| Nutrient Code | Description       | Django Model Field     |
|---------------|-------------------|------------------------|
| ENER-         | Calories          | calories               |
| FATNLEA       | Total Fat         | total_fat_g            |
| FAT           | Total Fat         | total_fat_g            |
| FASAT         | Saturated Fat     | saturated_fat_g        |
| FATRN         | Trans Fat         | trans_fat_g            |
| CHOL-         | Cholesterol       | cholesterol_mg         |
| NA            | Sodium            | sodium_mg              |
| CHO-          | Total Carbohydrate| total_carbohydrate_g   |
| FIBTSW        | Dietary Fiber     | dietary_fiber_g        |
| FIBR          | Dietary Fiber     | dietary_fiber_g        |
| SUGAR-        | Total Sugars      | total_sugars_g         |
| SUGAD         | Added Sugars      | added_sugars_g         |
| PRO-          | Protein           | protein_g              |
| VITD-         | Vitamin D         | vitamin_d_mcg          |
| CA            | Calcium           | calcium_mg             |
| FE            | Iron              | iron_mg                |
| K             | Potassium         | potassium_mg           |

## Known Food Product GTINs

We've identified several GTINs that reliably contain nutritional information:

- `00037600168526`: Hormel Chorizo
- `00028400083140`: Doritos
- `00018000428434`: Cheerios
- `00044000026882`: Pepsi
- `00079100851744`: Ritz Crackers

## Django Integration

To integrate with Django:

1. Install the package:
```bash
pip install oneworldsync
```

2. Add settings to your Django settings.py:
```python
# 1WorldSync API settings
ONEWORLDSYNC_APP_ID = 'your_app_id'
ONEWORLDSYNC_SECRET_KEY = 'your_secret_key'
ONEWORLDSYNC_USER_GLN = 'your_gln'  # Optional
```

3. Use the NutritionService in your Django views:
```python
from django.shortcuts import render
from .django_nutrition_service import NutritionService

def product_detail(request, gtin):
    service = NutritionService()
    product_data = service.get_product_nutrition(gtin)
    
    # Update your Django model
    product, created = Product.objects.update_or_create(
        gtin=gtin,
        defaults=product_data
    )
    
    return render(request, 'products/detail.html', {'product': product})
```

## Testing the Django Service

To test the Django-dependent service, create a script that sets up the Django environment:

```python
import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
sys.path.append('/path/to/your/django/project')

# Initialize Django
django.setup()

# Import the service
from django_nutrition_service import NutritionService

# Test the service
service = NutritionService()
product = service.get_product_nutrition("00037600168526")
print(f"Product: {product.get('name')}")
print(f"Calories: {product.get('calories')}")
```

## Limitations

- Not all products have complete nutritional information
- The structure of the data can vary between products
- Some nutrient codes may not be standardized across all products
- The GTIN field may not be populated in the API response

For more detailed information, refer to the official 1WorldSync API documentation.