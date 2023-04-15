from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, permissions, filters

from ecommerce import models, api_serializers


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Category.objects.all()
    serializer_class = api_serializers.CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)

    def get_permissions(self):
        # If action is list, no permissions needed. if action is create, client must be authenticated.
        if self.action == 'list':
            permission_classes = []
        else:  # if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProductViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Product.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('category', 'owner')
    search_fields = ('name', 'category__name')
    ordering_fields = ('price', 'name')

    def get_serializer_class(self):
        if self.action == 'list':
            return api_serializers.ProductReadSerializer
        elif self.action == 'create':
            return api_serializers.ProductWriteSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        # If action is list, no permissions needed. if action is create, client must be authenticated.
        if self.action == 'list':
            permission_classes = []
        else:  # if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
