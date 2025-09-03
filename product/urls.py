from django.urls import path
from product.views import category_list, product_detail, product_list_create, category_detail

urlpatterns = [
    path("categories/", category_list, name="category-list"),
    path("categories/<int:pk>/", category_detail, name="category-detail"),

    # Product
    path("products/", product_list_create, name="product-list-create"),
    path("products/<int:pk>/", product_detail, name="product-detail"),
]
