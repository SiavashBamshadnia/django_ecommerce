from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from ecommerce import models, api_serializers


def temporary_image():
    bts = BytesIO()
    img = Image.new("RGB", (100, 100))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())


class CategoryViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('category-list')
        self.user = get_user_model().objects.create_user(phone_number='9131111111', password='password')
        self.category1 = models.Category.objects.create(name='Category 1')
        self.category2 = models.Category.objects.create(name='Category 2')

    def test_list_categories(self):
        response = self.client.get(self.url)
        expected_response = api_serializers.CategorySerializer([self.category1, self.category2], many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_create_category(self):
        data = {'name': 'Category 3'}
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.url, data, headers={'Authorization': f'Bearer {refresh.access_token}'})
        expected_response = api_serializers.CategorySerializer(models.Category.objects.get(name='Category 3')).data

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Category.objects.count(), 3)
        self.assertEqual(response.json(), expected_response)

    def test_create_category_with_invalid_data(self):
        data = {'name': ''}
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.url, data, headers={'Authorization': f'Bearer {refresh.access_token}'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(models.Category.objects.count(), 2)

    def test_create_category_without_authorization_token(self):
        data = {'name': 'Category 3'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 401 | 403)
        self.assertEqual(models.Category.objects.count(), 2)

    def test_search_categories(self):
        response = self.client.get(self.url, {'search': 'Category 1'})
        expected_response = api_serializers.CategorySerializer([self.category1], many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)


class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.image_upload = temporary_image()
        self.url = reverse('product-list')
        self.user = get_user_model().objects.create_user(phone_number='9131111111', password='password')
        self.category1 = models.Category.objects.create(name='Category 1')
        self.product1 = models.Product.objects.create(name='Product 1', price=10000, stock=10, category=self.category1,
                                                      owner=self.user)
        self.product2 = models.Product.objects.create(name='Product 2', price=20000, stock=20, category=self.category1,
                                                      owner=self.user)

    def test_list_products(self):
        response = self.client.get(self.url)
        expected_response = api_serializers.ProductSerializer([self.product1, self.product2], many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    def test_create_product(self):
        data = {'name': 'Product 3', 'price': 3000, 'stock': 950, 'category': self.category1.id,
                'image': self.image_upload}
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.url, data, headers={'Authorization': f'Bearer {refresh.access_token}'})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Product.objects.count(), 3)
        self.assertEqual(models.Product.objects.last().owner, self.user)

    def test_create_product_with_invalid_data(self):
        data = {'name': 'Product 3', 'price': -1, 'stock': 950, 'category': self.category1.id,
                'image': self.image_upload}
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.url, data, headers={'Authorization': f'Bearer {refresh.access_token}'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(models.Product.objects.count(), 2)

    def test_create_product_without_authorization_token(self):
        data = {'name': 'Product 3', 'price': 3000, 'stock': 950, 'category': self.category1.id,
                'image': self.image_upload}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 401 | 403)
        self.assertEqual(models.Product.objects.count(), 2)

    def test_search_products(self):
        response = self.client.get(self.url, {'search': 'Product 2'})
        expected_response = api_serializers.ProductSerializer([self.product2], many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    def test_filter_products_by_category(self):
        response = self.client.get(self.url, {'category': self.category1.id})
        expected_response = api_serializers.ProductSerializer([self.product1, self.product2], many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    def test_filter_products_by_owner(self):
        user2 = get_user_model().objects.create_user(phone_number='9121111111', password='password')
        models.Product.objects.create(name='Product 3', price=3000, stock=400, category=self.category1, owner=user2)
        response = self.client.get(self.url, {'owner': self.user.id})
        expected_response = api_serializers.ProductSerializer([self.product1, self.product2], many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    def test_order_products_by_price(self):
        response = self.client.get(self.url, {'ordering': 'price'})
        expected_response = api_serializers.ProductSerializer([self.product1, self.product2], many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)

    def test_order_products_by_name(self):
        response = self.client.get(self.url, {'ordering': 'name'})
        expected_response = api_serializers.ProductSerializer([self.product1, self.product2], many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_response)
