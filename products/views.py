from .models import Product
from inventory.models import Inventory
from .serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
import datetime

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    authentication_classes = (TokenAuthentication,)

    # def get_serializer_class(self):
    #     if self.request.method == 'PUT':
    #         return ProductUpdateSerializer
    #     return ProductSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sfm_id = serializer.validated_data['style'] + '-' + serializer.validated_data['size'] + '-' + \
                 serializer.validated_data['color']
        # needed to perform validation on sfmId field also
        queryset = Product.objects.filter(sfmId=sfm_id)
        if queryset.exists():
            raise ValidationError(detail={"style": ["style-size-color already exists"]})
        new_product = serializer.save(sfmId=sfm_id)
        try:
            create_inventory_record(new_product)
        except:
            raise ValidationError(detail={"form": "Product saved but could not create inventory record"})
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

def create_inventory_record(p):
    new_inventory = Inventory(sfmId=p.sfmId, style=p.style, size=p.size, color=p.color, inStock=0, arrivalDate=datetime.date.today(), minimum=0, maximum=100)
    new_inventory.save()
