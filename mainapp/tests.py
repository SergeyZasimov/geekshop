from django.test import TestCase
from django.test.client import Client

from mainapp.models import ProductCategory, Product


class TestMainappSmoke(TestCase):

    success_code = 200
    error_code = 500

    def setUp(self):
        category = ProductCategory.objects.create(name='category 1')
        Product.objects.create(category=category, name='product 1')
        Product.objects.create(category=category, name='product 2')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.success_code)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, self.success_code)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, self.success_code)

    def test_mainapp_product_urls(self):
        response = self.client.get('/products/0/')
        self.assertEqual(response.status_code, self.success_code)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/{category.pk}/')
            self.assertEqual(response.status_code, self.success_code)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, self.success_code)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertNotEqual(response.status_code, self.error_code)

    def tearDown(self):
        pass
