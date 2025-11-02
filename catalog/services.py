from .models import Product

def get_products_by_category(category_id):
    """функция для получения продуктов по категории"""
    return Product.objects.filter(category_id=category_id, is_published=True)