from django.contrib import admin
from .models import Category, Product, ProductImage, SubCategory, BuyRequestImage, BuyRequest, Currency


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



class BuyRequestImageInline(admin.TabularInline):
    model = BuyRequestImage
    extra = 1
    fields = ("image",)
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" style="object-fit: cover;" />'
        return "(No image)"
    image_preview.allow_tags = True
    image_preview.short_description = "Preview"

# Currency admin
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name")
    search_fields = ("code", "name")


@admin.register(BuyRequest)
class BuyRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "user", "category", "status", "is_active", "created_at"
    )
    list_filter = ("status", "is_active", "category")
    search_fields = ("title", "description", "user__email")
    list_editable = ("status", "is_active")
    inlines = [BuyRequestImageInline]
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            "fields": ("user", "title", "description", "desired_price", 'currency', 'phone_number', "condition", "is_active")
        }),
        ("Kategoriyalar", {
            "fields": ("category", "subcategory")
        }),
        ("Joylashuv va holat", {
            "fields": ("location", "status")
        }),
        ("Vaqtlar", {
            "fields": ("created_at", "updated_at")
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user", "category", "subcategory")


@admin.register(BuyRequestImage)
class BuyRequestImageAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" style="object-fit: cover;" />'
        return "(No image)"
    image_preview.allow_tags = True
    image_preview.short_description = "Preview"
