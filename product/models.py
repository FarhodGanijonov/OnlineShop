from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="image_category/", blank=True, null=True)
    icon = models.ImageField(upload_to="icon_category/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='subcategories'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to="subcategory_icon/", blank=True, null=True)
    image = models.ImageField(upload_to="subcategory_image/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} → {self.title}"



class Product(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("inactive", "Inactive")
    ]

    CONDITION_CHOICES = [
        ("new", "New"),
        ("used", "Used"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    icon = models.ImageField(upload_to="product_icon", blank=True, null=True)
    emoji = models.ImageField(upload_to="product_emoji", blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # approval status
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default="new")  # new/used

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")  # products -> product
    image = models.ImageField(upload_to="products_image/", blank=True, null=True)

    def __str__(self):
        return self.product.title




class BuyRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("fulfilled", "Fulfilled"),
    ]

    CONDITION_CHOICES = [
        ("new", "New"),
        ("used", "Used"),
        ("any", "Any"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buy_requests"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    desired_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default="any")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="buy_requests")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name="buy_requests")
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.user.email})"


class BuyRequestImage(models.Model):
    request = models.ForeignKey(BuyRequest, on_delete=models.CASCADE, related_name="BuyRequest_images")  # products -> product
    image = models.ImageField(upload_to="BuyRequest_image/", blank=True, null=True)

    def __str__(self):
        return self.request.title
