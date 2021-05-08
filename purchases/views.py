from .models import Purchase
from .serializers import PurchaseSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
    authentication_classes = (TokenAuthentication,)

