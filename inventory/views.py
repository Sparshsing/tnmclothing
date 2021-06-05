from .models import Inventory
from .serializers import InventorySerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all().order_by('sfmId')
    authentication_classes = (TokenAuthentication,)

