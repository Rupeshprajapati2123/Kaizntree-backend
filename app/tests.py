from django.test import TestCase
from rest_framework.test import APIClient
from .models import Product

class GetProductsTestCase(TestCase):
    def setUp(self):
        # Create sample products in the database
        Product.objects.create(
            sku='ABC123',
            name='Product 1',
            category='Electronics',
            stock_status='In Stock',
            available_stock=50
        )
        Product.objects.create(
            sku='DEF456',
            name='Product 2',
            category='Clothing',
            stock_status='Out of Stock',
            available_stock=0
        )

    def test_get_products(self):
        # Initialize test client
        client = APIClient()

        # Make GET request to get-products endpoint
        response = client.get('/get-products/')

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Check response data
        data = response.json()
        self.assertEqual(len(data), 2)  # Ensure correct number of products returned
        self.assertEqual(data[0]['sku'], 'ABC123')  # Check SKU of first product
        self.assertEqual(data[0]['name'], 'Product 1')  # Check name of first product
        self.assertEqual(data[1]['sku'], 'DEF456')  # Check SKU of second product
        self.assertEqual(data[1]['name'], 'Product 2')  # Check name of second product

    def test_get_products_with_filters(self):
        # Initialize test client
        client = APIClient()

        # Make GET request to get-products endpoint with filters
        response = client.get('/get-products/', {'category': 'Electronics'})

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Check response data
        data = response.json()
        self.assertEqual(len(data), 1)  # Ensure correct number of products returned
        self.assertEqual(data[0]['sku'], 'ABC123')  # Check SKU of first product
        self.assertEqual(data[0]['name'], 'Product 1')  # Check name of first product
