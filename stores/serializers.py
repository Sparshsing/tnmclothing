from rest_framework import serializers
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('storeName', 'storeCode', 'emailAddress', 'addressLine1', 'addressLine2', 'city', 'state', 'zipCode', 'user', 'userFullName')
        read_only_fields = ['userFullName']