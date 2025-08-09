from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from .filters import ProductFilter


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all() #query-set
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data, status=200)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
     queryset = Product.objects.all()
     serializer_class = ProductSerializer
     lookup_field = 'pk'

     def get_permissions(self):
         self.permission_classes = [AllowAny]

         if self.request.method in ['PATCH', 'PUT', 'DELETE']:
             self.permission_classes = [IsAdminUser]
         return super().get_permissions()

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items').all()
    serializer_class = OrderSerializer


#     @api_view(['GET'])
#     def product_list_by_user(request):
#     user = request.user
#     order = Order.objects.filter(user=user)
#     serializer = OrderSerializer(order, many=True)
#     return Response(serializer.data)


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
      
# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('items').all()
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


class ProductInfoAPIView(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)





# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer(
#         {
#             'products': products,
#             'count': len(products),
#             'max_price': products.aggregate(max_price=Max('price'))['max_price']
#         }
#     )
#     return Response(serializer.data)