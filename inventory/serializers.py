from rest_framework import serializers
from .models import Inventory

class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ('id', 'sfmId', 'style', 'size', 'color', 'inStock', 'arrivalDate', 'minimum', 'maximum', 'inTransit', 'unfulfilledCount', 'productAvailability', 'trueCount', 'shortCount', 'needToPurchase')
        # extra_kwargs = {'productAvailability': {'read_only': True, 'default': 'not bad'}
        #                 }

class InventoryListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    sfmId = serializers.CharField()
    style = serializers.CharField()
    size = serializers.CharField()
    color = serializers.CharField()
    inStock = serializers.IntegerField()
    arrivalDate = serializers.DateField()
    minimum = serializers.IntegerField()
    maximum = serializers.IntegerField()
    inTransit = serializers.IntegerField()
    unfulfilledCount = serializers.IntegerField()
    # comment these calculated fields for performance, calculate in client
    # productAvailability = serializers.CharField()
    # trueCount = serializers.IntegerField()
    # shortCount = serializers.IntegerField()
    # needToPurchase = serializers.IntegerField()