from rest_framework import serializers
from .models import Purchase

class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ('status', 'style', 'size', 'color', 'company', 'warehouse', 'ordered', 'orderDate', 'arrivalDate', 'sfmId')