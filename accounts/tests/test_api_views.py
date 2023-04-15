import json

from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse
from django.utils import lorem_ipsum

from accounts import models


class TestApiViews(TestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_registration_view(self):
        data = {
            'name': lorem_ipsum.words(2),
            'sex': 'F',
            'birth_date': '1995-01-23',
            'phone_number': '9131111111',
            'password': 'fKj#8Lp@5tDm',
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.User.objects.count(), 1)
        self.assertNotEqual(authenticate(phone_number=data['phone_number'], password=data['password']), None)

    def test_registration_view_with_repetitive_phone_number(self):
        models.User.objects.create_user('9131111111', 'password')
        response = self.client.post(self.url, {
            'name': lorem_ipsum.words(2),
            'sex': 'F',
            'birth_date': '1995-01-23',
            'phone_number': '9131111111',
            'password': 'fKj#8Lp@5tDm',
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(models.User.objects.count(), 1)

    def test_registration_view_without_required_fields(self):
        response = self.client.post(self.url, {
            'name': lorem_ipsum.words(2),
            'sex': 'F',
            'birth_date': '1995-01-23',
        })
        response_content: dict = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('phone_number' in response_content)
        self.assertTrue('password' in response_content)
        self.assertEqual(len(response_content), 2)
        self.assertEqual(models.User.objects.count(), 0)

    def test_registration_view_with_blank_required_fields(self):
        response = self.client.post(self.url, {
            'name': lorem_ipsum.words(2),
            'sex': 'F',
            'birth_date': '1995-01-23',
            'phone_number': '',
            'password': '',
        })
        response_content: dict = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('phone_number' in response_content)
        self.assertTrue('password' in response_content)
        self.assertEqual(len(response_content), 2)
        self.assertEqual(models.User.objects.count(), 0)

    def test_registration_view_with_invalid_data(self):
        response = self.client.post(self.url, {
            'name': lorem_ipsum.words(2),
            'sex': 'a',
            'birth_date': lorem_ipsum.words(1),
            'phone_number': '123',
            'password': 'abcd',
        })
        response_content: dict = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('sex' in response_content)
        self.assertTrue('birth_date' in response_content)
        self.assertTrue('phone_number' in response_content)
        self.assertEqual(len(response_content), 3)
        self.assertEqual(models.User.objects.count(), 0)

    def test_registration_view_with_unsecure_password(self):
        response = self.client.post(self.url, {
            'name': lorem_ipsum.words(2),
            'sex': 'F',
            'birth_date': '1995-01-23',
            'phone_number': '9131111111',
            'password': 'abcd',
        })
        response_content: dict = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('password' in response_content)
        self.assertEqual(len(response_content), 1)
        self.assertEqual(models.User.objects.count(), 0)
