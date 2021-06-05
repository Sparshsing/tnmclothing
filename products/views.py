from .models import Product
from inventory.models import Inventory
from .serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import BasePermission, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from .business_logic import Utilities
import pandas as pd
from rest_framework import permissions
import logging

# Get an instance of a logger
logger = logging.getLogger('db')

class ProductPermission(BasePermission):
    def has_permission(self, request, view):
        print(view.action)
        if view.action=='import_file':
            return (request.user.is_superuser or request.user.is_staff)
        if view.action=='list':
            return True
        return (request.user.is_superuser or request.user.is_staff)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('sfmId')
    authentication_classes = (TokenAuthentication,)
    permission_classes = [ProductPermission]
    # def get_serializer_class(self):
    #     if self.request.method == 'PUT':
    #         return ProductUpdateSerializer
    #     return ProductSerializer

    def create(self, request, *args, **kwargs):
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
            Utilities.create_inventory_record(new_product)
            logger.info(request.user.username + ' created product ' + sfm_id + 'and an inventory record created automatically')
        except:
            logger.error(request.user.username + ' created product ' + sfm_id + 'but inventory creation failed')
            raise ValidationError(detail={"form": "Product saved but could not create inventory record"})
        headers = self.get_success_headers(serializer.data)
        logger.info(request.user.username + ' created product ' + sfm_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        sfmId = str(instance.sfmId)
        instance.delete()
        try:
            inv = Inventory.objects.get(sfmId=sfmId)
            inv.delete()
            logger.info(self.request.user.username + ' deleted product ' + sfmId + ' and inventory record was deleted automatically.')
        except Exception as e:
            logger.error(self.request.user.username + ' deleted product ' + sfmId + ' but inventory not deleted. Maybe inventory record was not there')
            print(e)

    def perform_update(self, serializer):
        logger.info(
            self.request.user.username + ' updated product ' + serializer.data['sfmId'])
        serializer.save()

    @action(detail=False, methods=['POST'])
    def import_file(self, request, pk=None):

        myfile = request.FILES['productsFile']

        if '.csv' in myfile.name:
            data = pd.read_csv(myfile)
            print(data.head())
            errors = Utilities.import_products(data)
            print(errors)
        if '.xlsx' in myfile.name:
            data = pd.read_excel(myfile, engine='openpyxl')
            print(data.head())
            errors = Utilities.import_products(data)
            print(errors)
        if len(errors) == 0:
            logger.info(request.user.username + ' imported products file ' + str(myfile.name))
        else:
            errorstring = ','.join(errors)
            errorstring = errorstring[:200] + '...' if len(errorstring) > 200 else errorstring
            logger.exception(request.user.username + ' imported products file ' + str(myfile.name) + ' with errors ' + errorstring)
        return Response({'errors': errors})


