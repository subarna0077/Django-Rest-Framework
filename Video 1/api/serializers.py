from rest_framework import serializers
from django.db import transaction

from .models import Product, Order, OrderItem, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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
    
class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')
        
    items = OrderItemCreateSerializer(many=True)

    def update(self, instance, validated_data):
        orderitem_data = validated_data.pop('items')
        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if orderitem_data is not None:
                instance.items.all().delete()

                ##Recreate items with the updated data

                for item in orderitem_data:
                    OrderItem.objects.create(order=instance, **item)

            return instance
        
    with transaction.atomic():
        def create(self, validated_data):
            orderitem_data = validated_data.pop('items')
            order = Order.objects.create(**validated_data)

            for item in orderitem_data:
                OrderItem.objects.create(order = order, **item)

            return order

    class Meta:
         fields = ['user', 'status', 'items']
         model = Order

         extra_kwargs={
             'user': {'read_only': True}
         }


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only = True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    class Meta:
        model = Order
        fields = ['order_id', 'user', 'status', 'created_at', 'items', 'total_price']

class ProductInfoSerializer(serializers.Serializer):
    #get all products, count of products, max price
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
