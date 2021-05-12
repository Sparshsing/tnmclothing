from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('sfmId', 'style', 'size', 'color', 'sku', 'cost', 'price', 'amountInStock')
        read_only_fields = ['sfmId', 'amountInStock']

# class ProductUpdateSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Product
#         fields = ('sfmId', 'style', 'size', 'color', 'sku', 'cost', 'price', 'amountInStock')
#         read_only_fields = ['sfmId', 'amountInStock', 'style', 'size', 'color']

