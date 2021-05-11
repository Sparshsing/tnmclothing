from rest_framework import serializers
from .models import Purchase
from datetime import date, timedelta


class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ('id', 'status', 'style', 'size', 'color', 'company', 'warehouse', 'ordered', 'orderDate', 'arrivalDate', 'sfmId')
        extra_kwargs = {'arrivalDate': {'read_only': True, 'default': date.today()},
                        'sfmId': {'read_only': True, 'default': 'style' + '-' + 'size' + 'color'}}

