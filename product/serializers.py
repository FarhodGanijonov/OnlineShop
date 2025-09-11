from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Category’ni detailda ko‘rsatish
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    user = serializers.ReadOnlyField(source="user.email")  # kim qo‘shganini ko‘rsatish


    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "image", "location",
                  "created_at", "updated_at", "is_active", "category", "category_id", "user",]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user
        return super().create(validated_data)
