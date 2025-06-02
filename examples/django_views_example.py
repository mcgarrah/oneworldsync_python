"""
Example Django views for using the NutritionService.
"""

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .django_nutrition_service import NutritionService
from products.models import Product

def product_nutrition(request, gtin):
    """View to display nutritional information for a product."""
    # Get or create the product
    product, created = Product.objects.get_or_create(
        gtin=gtin,
        defaults={'name': f'Product {gtin}'}
    )
    
    # If product doesn't have nutritional info, fetch it
    if not product.calories:
        service = NutritionService()
        nutrition = service.get_product_nutrition(gtin)
        
        if nutrition:
            # Update product with nutritional information
            for field, value in nutrition.items():
                if hasattr(product, field):
                    setattr(product, field, value)
            
            product.save()
    
    return render(request, 'products/detail.html', {'product': product})

def import_food_products(request):
    """View to import food products with nutritional information."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    segment_code = request.POST.get('segment_code', '50030000')
    
    service = NutritionService()
    products = service.get_food_products(segment_code=segment_code)
    
    imported_count = 0
    for product_data in products:
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

def food_segments_list(request):
    """View to list available food segments."""
    service = NutritionService()
    
    return JsonResponse({
        'segments': service.FOOD_SEGMENTS
    })