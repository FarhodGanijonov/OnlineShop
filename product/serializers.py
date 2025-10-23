from rest_framework import serializers
from .models import Category, SubCategory, Product, ProductImage

# Category serializer
class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Category
        fields = "__all__"

# SubCategory serializer
class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    created_at = serializers.SerializerMethodField()


    class Meta:
        model = SubCategory
        fields = ["id", "title", "description", "icon", "image", "category", "category_id", 'created_at']

    def get_created_at(self, obj):
        return obj.created_at.date()  # faqat YYYY-MM-DD


# ProductImage serializer
class ProductsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"

# Product serializer
class ProductSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format="%Y-%m-%d", read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    subcategory = SubCategorySerializer(read_only=True)
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(), source="subcategory", write_only=True
    )

    user = serializers.ReadOnlyField(source="user.email")

    images = ProductsImageSerializer(many=True, read_only=True)
    images_upload = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            "id", "title", "description", "price", "icon", "emoji", "condition", "location",
            "created_at", "updated_at", "is_active", "category", "category_id",
            "subcategory", "subcategory_id",
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

        # Save uploaded images
        for img in images_data:
            ProductImage.objects.create(product=product, image=img)

        return product
