from django.urls import path
from product.views import category_list, product_list_create, category_detail, product_detail_get, \
    product_detail_update_delete, toggle_product_active

urlpatterns = [
    path("categories/", category_list, name="category-list"),
    path("categories/<int:pk>/", category_detail, name="category-detail"),

    # Product
    path("products/", product_list_create, name="product-list-create"),
    path("products/<int:pk>/", product_detail_get, name="product-detail-get"),
    path("products/<int:pk>/edit/and/delete/", product_detail_update_delete, name="product-detail-update-delete"),
    path("products/<int:pk>/toggle_active/", toggle_product_active, name="toggle_product_active"),

]
