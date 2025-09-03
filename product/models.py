from django.db import models
from rest_framework import settings


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)  # masalan: "Toshkent, Yunusobod"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
