from django.contrib import admin

from ecommerce import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = list_display
    search_fields = ('name',)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'owner')
    list_display_links = list_display
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'owner')
