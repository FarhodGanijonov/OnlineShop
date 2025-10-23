from django.urls import path

from product import views

urlpatterns = [
    # Category API
    path('categories/', views.category_list, name='category-list'),                  # Barcha categorylar
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),     # Category detail

    #  SubCategory API
    path('subcategories/', views.subcategory_list, name='subcategory-list'),         # ?category=ID bo'yicha subcategory list

    # Product API
    path('products/', views.product_list_create, name='product-list-create'),        # GET/POST product list va create
    path('products/<int:pk>/', views.product_detail_get, name='product-detail'),    # Product detail
    path('products/<int:pk>/edit/', views.product_detail_update_delete, name='product-update-delete'), # PUT/DELETE

    # Products by SubCategory
    path('subcategories/<int:subcategory_id>/products/', views.products_by_subcategory, name='products-by-subcategory'),
    path("products/<int:pk>/toggle_active/", views.toggle_product_active, name="toggle_product_active"),

]
