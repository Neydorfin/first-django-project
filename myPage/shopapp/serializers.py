from rest_framework import serializers
from .models import Order, Product


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('pk', 'delivery_address', 'promocode', 'created_at', 'user',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('pk', 'name', 'description', 'price', 'discount',
                  'created_by_id', 'created_at', 'archived', 'images',)
