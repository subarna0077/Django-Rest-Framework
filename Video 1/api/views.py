from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max
from rest_framework import generics


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all() #query-set
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data, status=200)

class ProductDetailAPIView(generics.RetrieveAPIView):
     queryset = Product.objects.all()
     serializer_class = ProductSerializer
     lookup_field = 'pk'

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items').all()
    serializer_class = OrderSerializer


# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('items').all()
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer(
        {
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        }
    )
    return Response(serializer.data)
