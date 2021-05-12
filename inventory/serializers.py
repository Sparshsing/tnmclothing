from rest_framework import serializers
from .models import Inventory

class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ('sfmId', 'style', 'size', 'color', 'inStock', 'arrivalDate', 'minimum', 'maximum', 'inTransit', 'unfulfilledCount', 'productAvailability', 'trueCount', 'shortCount', 'needToPurchase')
        # extra_kwargs = {'productAvailability': {'read_only': True, 'default': 'not bad'}
        #                 }