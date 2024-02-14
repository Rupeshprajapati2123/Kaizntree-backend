# utils.py

import json
from .models import Product

def save_products_to_database(data):
    for item in data:
        product = Product.objects.create(
            sku=item.get('SKU'),
            name=item.get('name'),
            category=item.get('category'),
            tags=json.dumps(item.get('tags', [])),
            stock_status=item.get('stock_status'),
            available_stock=item.get('available_stock')
        )
        if 'date_created' in item:  # Check if date_created is present in the item
            product.date_created = item['date_created']
            product.save()


def fetch_products_from_database():
    products = Product.objects.all()
    data = []
    for product in products:
        product_data = {
            'SKU': product.sku,
            'name': product.name,
            'category': product.category,
            'tags': json.loads(product.tags),
            'stock_status': product.stock_status,
            'available_stock': product.available_stock
        }
        if hasattr(product, 'date_created'):
            product_data['date_created'] = product.date_created.strftime("%Y-%m-%d %H:%M:%S")
        data.append(product_data)
    return data
