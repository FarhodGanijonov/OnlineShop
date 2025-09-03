from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


# -------- Category Views --------
@api_view(["GET"])
@permission_classes([AllowAny])
def category_list(request):
    categories = Category.objects.all().order_by("-created_at")
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)


# -------- Product Views --------
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def product_list_create(request):
    if request.method == "GET":
        products = Product.objects.filter(is_active=True).order_by("-created_at")

        # filter: ?category=1
        category_id = request.GET.get("category")
        if category_id:
            products = products.filter(category_id=category_id)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  #  user avtomatik yoziladi
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])  # faqat owner o‘z productini update/delete qila oladi
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == "PUT":
        if product.user != request.user:
            return Response({"error": "Siz faqat o‘z mahsulotingizni o‘zgartira olasiz"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        if product.user != request.user:
            return Response({"error": "Siz faqat o‘z mahsulotingizni o‘chira olasiz"},
                            status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
