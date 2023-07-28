from rest_framework import serializers

from accounts.api_serializers import UserSerializer
from ecommerce import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'
