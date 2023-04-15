import rest_framework_simplejwt.views as jwt_views
from django.test import TestCase
from django.urls import resolve

from accounts import api_views


class TestApiUrls(TestCase):
    def test_token_api_url(self):
        url = '/api/accounts/token/'

        self.assertEqual(resolve(url).func.view_class, jwt_views.TokenObtainPairView)

    def test_token_refresh_api_url(self):
        url = '/api/accounts/token/refresh/'

        self.assertEqual(resolve(url).func.view_class, jwt_views.TokenRefreshView)

    def test_token_verify_api_url(self):
        url = '/api/accounts/token/verify/'

        self.assertEqual(resolve(url).func.view_class, jwt_views.TokenVerifyView)

    def test_token_blacklist_api_url(self):
        url = '/api/accounts/token/blacklist/'

        self.assertEqual(resolve(url).func.view_class, jwt_views.TokenBlacklistView)

    def test_register_api_url(self):
        url = '/api/accounts/register/'

        self.assertEqual(resolve(url).func.view_class, api_views.RegistrationView)
