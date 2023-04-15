import rest_framework_simplejwt.views as jwt_views
from django.urls import path

from accounts import api_views

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', jwt_views.TokenBlacklistView.as_view(), name='token_blacklist'),

    path('register/', api_views.RegistrationView.as_view(), name='register'),
]
