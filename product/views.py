from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Category, Product, SubCategory, BuyRequest
from .serializers import CategorySerializer, ProductSerializer, SubCategorySerializer, BuyRequestSerializer


# category ga tegishli subkategory ni olish
@api_view(["GET"])
@permission_classes([AllowAny])
def subcategory_list(request):
    category_id = request.GET.get("category")  # ?category=1
    if not category_id:
        return Response({"detail": "Category ID required"}, status=400)

    subcategories = SubCategory.objects.filter(category_id=category_id).order_by("title")
    serializer = SubCategorySerializer(subcategories, many=True, context={'request': request})
    return Response(serializer.data)

# subcategory ga tegishli product listini olish
@api_view(["GET"])
@permission_classes([AllowAny])
def products_by_subcategory(request, subcategory_id):
    products = Product.objects.filter(subcategory_id=subcategory_id, status="approved", is_active=True)
    serializer = ProductSerializer(products, many=True, context={"request": request})
    return Response(serializer.data)

# category list
@api_view(["GET"])
@permission_classes([AllowAny])
def category_list(request):
    categories = Category.objects.all().order_by("-created_at")
    serializer = CategorySerializer(categories, many=True, context={'request':request})
    return Response(serializer.data)

# category detail
@api_view(["GET"])
@permission_classes([AllowAny])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category, context={'request':request})
    return Response(serializer.data)

# product post/get + filter
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

            elif status_filter in ["pending", "rejected", "inactive"]:
                if request.user.is_authenticated:
                    if status_filter == "inactive":
                        products = products.filter(user=request.user, is_active=False)
                    else:
                        products = products.filter(user=request.user, status=status_filter)
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

# product detail
@api_view(["GET"])
@permission_classes([AllowAny])  # GET uchun hammaga ruxsat
def product_detail_get(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product, context={"request": request})
    return Response(serializer.data)

# product put/delete
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


@api_view(["GET", "POST"])
def buy_request_list_create(request):
    if request.method == "GET":
        status_filter = request.GET.get("status")
        user_only = request.GET.get("my")

        buy_requests = BuyRequest.objects.all().order_by("-created_at")

        if request.user.is_authenticated:
            # Agar user umumiy ko‘rish qilsa (admin bo‘lmasa)
            if not request.user.is_staff:  # normal user
                # Foydalanuvchi faqat approved va active buy requestlarni ko‘radi
                buy_requests = buy_requests.filter(status="approved", is_active=True)
            else:
                # Admin yoki staff hamma statuslarni ko‘rishi mumkin
                if status_filter:
                    if status_filter in ["pending", "approved", "rejected", "fulfilled", "inactive"]:
                        if status_filter == "inactive":
                            buy_requests = buy_requests.filter(user=request.user, is_active=False)
                        else:
                            buy_requests = buy_requests.filter(user=request.user, status=status_filter)
        else:
            # Auth bo‘lmagan user ham approved va active buy requestlarni ko‘radi
            buy_requests = buy_requests.filter(status="approved", is_active=True)

        # Foydalanuvchining o‘z requestlari
        if user_only == "true" and request.user.is_authenticated:
            buy_requests = buy_requests.filter(user=request.user)

        serializer = BuyRequestSerializer(buy_requests, many=True, context={"request": request})
        return Response(serializer.data)

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=401)

        serializer = BuyRequestSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            buy_request = serializer.save()
            return Response({
                "message": "Buy request created successfully!",
                "buy_request": BuyRequestSerializer(buy_request, context={"request": request}).data
            }, status=201)
        return Response(serializer.errors, status=400)
