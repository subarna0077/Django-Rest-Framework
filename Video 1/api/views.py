from django.db.models import Max
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from api.models import Order, OrderItem, Product, User
from api.serializers import (OrderItemSerializer, OrderSerializer,
                             ProductInfoSerializer, ProductSerializer, OrderCreateSerializer, UserSerializer)

from .filters import OrderFilter, ProductFilter


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['= name', 'description']
    ordering_fields = ['name', 'price', 'stock']

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

#class OrderListAPIView(generics.ListAPIView):
#    queryset = Order.objects.prefetch_related('items').all()
#    serializer_class = OrderSerializer


#     @api_view(['GET'])
#     def product_list_by_user(request):
#     user = request.user
#     order = Order.objects.filter(user=user)
#     serializer = OrderSerializer(order, many=True)
#     return Response(serializer.data)


"""
class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
"""

      
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

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return OrderCreateSerializer
        
        
        return super().get_serializer_class()

    def get_queryset(self):
        qs=  super().get_queryset() #getting the base qs
        print(qs)
        if not self.request.user.is_staff: #if they are not a admin user:
            qs = qs.filter(user = self.request.user) # filter the qs specific to that user
        return qs
    
    def perform_create(self, serializer):
        serializer.save(user= self.request.user)
    

    #use filtering in a viewset


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None