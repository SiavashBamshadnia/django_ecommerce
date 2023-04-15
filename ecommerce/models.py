from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.PositiveBigIntegerField()
    stock = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='product_images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
