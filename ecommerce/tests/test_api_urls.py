from django.test import TestCase
from django.urls import resolve

from ecommerce import api_views


class TestApiUrls(TestCase):
    def test_categories_api_url(self):
        url = '/api/ecommerce/categories/'

        self.assertEqual(resolve(url).func.cls, api_views.CategoryViewSet)

    def test_products_api_url(self):
        url = '/api/ecommerce/products/'

        self.assertEqual(resolve(url).func.cls, api_views.ProductViewSet)
