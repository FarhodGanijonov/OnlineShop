from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def category_list(request):
    categories = Category.objects.all().order_by("-created_at")
    serializer = CategorySerializer(categories, many=True, context={'request':request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category, context={'request':request})
    return Response(serializer.data)


@api_view(["GET", "POST"])
def product_list_create(request):
    if request.method == "GET":
        status_filter = request.GET.get("status")  # ?status=pending kabi
        user_only = request.GET.get("my")  # ?my=true

        products = Product.objects.all().order_by("-created_at")

        # Filtrlash
        if status_filter:
            if status_filter == "approved":
                products = products.filter(status="approved", is_active=True)

            elif status_filter in ["pending", "rejected"]:
                if request.user.is_authenticated:
                    products = products.filter(user=request.user, status=status_filter)
                else:
                    return Response({"detail": "Authentication required."}, status=401)

            elif status_filter == "inactive":
                if request.user.is_authenticated:
                    products = products.filter(user=request.user, is_active=False)
                else:
                    return Response({"detail": "Authentication required."}, status=401)
        else:
            # Default holatda approved + active ko‘rsatiladi
            products = products.filter(status="approved", is_active=True)

        # Foydalanuvchining o‘z e’lonlari
        if user_only == "true" and request.user.is_authenticated:
            products = products.filter(user=request.user)

        # ?category=ID filtri
        category_id = request.GET.get("category")
        if category_id:
            products = products.filter(category_id=category_id)

        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            product = serializer.save(user=request.user, status="pending")
            return Response({
                "message": "E'lon yuborildi. Admin tasdiqlagandan so'ng saytda ko'rinadi!",
                "product": ProductSerializer(product, context={"request": request}).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])  # GET uchun hammaga ruxsat
def product_detail_get(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product, context={"request": request})
    return Response(serializer.data)


@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])  # faqat login bo‘lgan user
def product_detail_update_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.user != request.user:
        return Response({"error": "Siz faqat o‘z mahsulotingizni o‘zgartira/ o‘chira olasiz"},
                        status=status.HTTP_403_FORBIDDEN)

    if request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# User faqat ozining productini faollashtirish/yashirish mumkin
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def toggle_product_active(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.user != request.user:
        return Response({"detail": "Siz faqat o'z e'lonlaringizni boshqara olasiz."},
                        status=status.HTTP_403_FORBIDDEN)

    product.is_active = not product.is_active
    product.save(update_fields=["is_active"])

    status_msg = "E'lon faollashtirildi" if product.is_active else "E'lon yashirildi"
    return Response({
        "message": status_msg,
        "product": ProductSerializer(product, context={"request": request}).data
    })
