from .models import Product
from .serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = (TokenAuthentication,)

