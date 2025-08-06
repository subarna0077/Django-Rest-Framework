from rest_framework import serializers

from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'in_stock']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product_name', 'product_price', 'quantity', 'item_subtotal']

    def get_product_name(self, obj):
        return obj.product.name
    
    def get_product_price(self, obj):
        return obj.product.price


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['order_id', 'status', 'created_at', 'items']

