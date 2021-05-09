from .models import Order
from .serializers import OrderSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = (TokenAuthentication,)

