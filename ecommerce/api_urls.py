from django.urls import path, include
from rest_framework import routers

from ecommerce import api_views

router = routers.DefaultRouter()
router.register('categories', api_views.CategoryViewSet)
router.register('products', api_views.ProductViewSet)

urlpatterns = (path('', include(router.urls)),)
