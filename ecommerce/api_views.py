from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions

from ecommerce import models, api_serializers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = api_serializers.CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = api_serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('category', 'owner')
    search_fields = ('name', 'category__name')
    ordering_fields = ('price', 'name')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
