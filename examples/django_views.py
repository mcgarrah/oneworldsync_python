"""
Example Django views for using the NutritionService.
"""

from django.shortcuts import render
from django.http import JsonResponse
from .django_nutrition_service import NutritionService

def product_detail(request, gtin):
    """View to display nutritional information for a product."""
    from products.models import Product
    
    # Try to get product from database
    try:
        product = Product.objects.get(gtin=gtin)
        has_nutrition = bool(product.calories)
    except Product.DoesNotExist:
        product = Product(gtin=gtin)
        has_nutrition = False
    
    # If product doesn't have nutritional info, fetch it
    if not has_nutrition:
        service = NutritionService()
        nutrition_data = service.get_product_nutrition(gtin)
        
        if nutrition_data:
            # Update product with nutritional information
            for field, value in nutrition_data.items():
                if hasattr(product, field):
                    setattr(product, field, value)
            
            # Save the product
            product.save()
    
    return render(request, 'products/detail.html', {'product': product})

def import_sample_products(request):
    """View to import sample food products with nutritional information."""
    from products.models import Product
    
    service = NutritionService()
    products_data = service.get_sample_food_products()
    
    imported_count = 0
    for product_data in products_data:
        gtin = product_data.pop('gtin', None)
        if not gtin:
            continue
        
        # Get or create product
        product, created = Product.objects.update_or_create(
            gtin=gtin,
            defaults=product_data
        )
        
        imported_count += 1
    
    return JsonResponse({
        'success': True,
        'imported': imported_count
    })