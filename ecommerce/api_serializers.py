from rest_framework import serializers

from ecommerce import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class ProductReadSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    owner = serializers.StringRelatedField()

    class Meta:
        model = models.Product
        fields = '__all__'


class ProductWriteSerializer(serializers.ModelSerializer):
    # Price and stock must be positive
    price = serializers.IntegerField(min_value=0)
    stock = serializers.IntegerField(min_value=0)

    class Meta:
        model = models.Product
        exclude = ('owner',)
