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


class ProductsModelsTestCase(TestCase):
    """
    Тестирование методов моделей
    """

    def setUp(self):
        category = ProductCategory.objects.create(name='столы')
        self.product1 = Product.objects.create(name='стол 1',
                                               category=category,
                                               price=1000.5,
                                               quantity=5)

        self.product2 = Product.objects.create(name='стол 2',
                                               category=category,
                                               price=2000.1,
                                               quantity=4,
                                               is_active=False)

        self.product3 = Product.objects.create(name='стол 3',
                                               category=category,
                                               price=3000.5,
                                               quantity=1)

    def test_products_get(self):
        prod1 = Product.objects.get(name='стол 1')
        prod2 = Product.objects.get(name='стол 2')

        self.assertEqual(prod1, self.product1)
        self.assertEqual(prod2, self.product2)

    def test_product_print(self):
        prod1 = Product.objects.get(name='стол 1')
        prod2 = Product.objects.get(name='стол 2')

        self.assertEqual(str(prod1), 'стол 1 (столы)')
        self.assertEqual(str(prod2), 'стол 2 (столы)')

    def test_products_get_item(self):
        prod1 = Product.objects.get(name='стол 1')
        prod3 = Product.objects.get(name='стол 3')
        products = prod1.get_items()

        self.assertEqual(list(products), [prod1, prod3])

