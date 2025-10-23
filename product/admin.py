from django.contrib import admin
from .models import Category, Product, ProductImage, SubCategory


# Inline admin for images
class ProductImageInline(admin.TabularInline):  # yoki admin.StackedInline
    model = ProductImage
    extra = 1  # yangi rasm qo‘shish uchun bo‘sh satr soni


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    ordering = ("-created_at",)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "category")
    search_fields = ("title", "category__name")
    list_filter = ("category",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "is_active", "created_at")
    list_filter = ("status", "is_active", "category")
    search_fields = ("title", "description", "user__email")
    list_editable = ("status", "is_active")  # Admin paneldan to‘g‘ridan-to‘g‘ri statusni o‘zgartirish
    inlines = [ProductImageInline]  # shu yerga inline qo‘shamiz

