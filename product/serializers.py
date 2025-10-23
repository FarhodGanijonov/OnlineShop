from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    user = serializers.ReadOnlyField(source="user.email")

    #  Nested serializer for images
    images = ProductsImageSerializer(many=True, read_only=True)  # read-only, GET uchun
    images_upload = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )  # POST/PUT uchun rasm yuborish

    class Meta:
        model = Product
        fields = [
            "id", "title", "description", "price", 'icon', 'emoji', "location",
            "created_at", "updated_at", "is_active", "category", "category_id",
            "user", "status", "images", "images_upload"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "status", "images"]

    def create(self, validated_data):
        request = self.context.get("request")
        images_data = validated_data.pop("images_upload", [])
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user
            validated_data["status"] = "pending"

        product = super().create(validated_data)

        # 🔹 Save uploaded images
        for img in images_data:
            ProductImage.objects.create(product=product, image=img)

        return product
