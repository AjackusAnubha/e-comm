from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, Order
from django.urls import reverse

class ProductListCreateAPIViewTests(APITestCase):

    def setUp(self):
        self.product1 = Product.objects.create(name="Product 1", price=10.0, stock=100)
        self.product2 = Product.objects.create(name="Product 2", price=20.0, stock=50)
        self.url = reverse('product-list-create')

    def test_get_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Product 1')
        self.assertEqual(response.data[1]['name'], 'Product 2')

    def test_create_product(self):
        data = {
            'name': 'Product 3',
            'description': 'Product 3 description',
            'price': 15.0,
            'stock': 30
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(Product.objects.get(id=response.data['id']).name, 'Product 3')


class OrderCreateAPIViewTests(APITestCase):

    def setUp(self):
        self.product1 = Product.objects.create(name="Product 1", price=10.0, stock=100)
        self.product2 = Product.objects.create(name="Product 2", price=20.0, stock=50)
        self.url = reverse('order-create')

    def test_create_order(self):
        data = {
            'products': [
                {'product_id': self.product1.id, 'quantity': 2},
                {'product_id': self.product2.id, 'quantity': 1}
            ],
            'status': 'pending'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=response.data['id'])
        self.assertEqual(order.total_price, 40.0)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(Product.objects.get(id=self.product1.id).stock, 98)
        self.assertEqual(Product.objects.get(id=self.product2.id).stock, 49)

    def test_order_with_insufficient_stock(self):
        data = {
            'products': [
                {'product_id': self.product1.id, 'quantity': 101},
                {'product_id': self.product2.id, 'quantity': 1}
            ],
            'status': 'pending'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], f"Insufficient stock for product {self.product1.name}.")

    def test_order_with_non_existent_product(self):
        data = {
            'products': [
                {'product_id': 999, 'quantity': 2},
                {'product_id': self.product2.id, 'quantity': 1}
            ],
            'status': 'pending'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], "Product with ID 999 does not exist.")

    def test_order_with_invalid_quantity(self):
        data = {
            'products': [
                {'product_id': self.product1.id, 'quantity': -1},
                {'product_id': self.product2.id, 'quantity': 1}
            ],
            'status': 'pending'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_with_zero_quantity(self):
        data = {
            'products': [
                {'product_id': self.product1.id, 'quantity': 0},
                {'product_id': self.product2.id, 'quantity': 1}
            ],
            'status': 'pending'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
