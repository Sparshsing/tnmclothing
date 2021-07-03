from rest_framework import pagination, filters

from .models import Purchase
from .serializers import PurchaseSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from .business_logic import Utilities
import pandas as pd
from datetime import timedelta
import logging

# Get an instance of a logger
logger = logging.getLogger('db')

# Create your views here.

class PurchasePagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all().order_by('-id')
    authentication_classes = (TokenAuthentication,)
    pagination_class = PurchasePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['style', 'size', 'color', 'warehouse', 'company']


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sfm_id = serializer.validated_data['style'] + '-' + serializer.validated_data['size'] + '-' + serializer.validated_data['color']
        days_add = 10 if serializer.validated_data['warehouse'].upper() == 'BE' else 5
        arrival_date = serializer.validated_data['orderDate'] + timedelta(days=days_add)
        new_purchase = serializer.save(arrivalDate=arrival_date, sfmId=sfm_id)
        try:
            Utilities.update_inventory(new_purchase)
        except:
            logger.error(request.user.username + ' created purchase id ' + str(new_purchase.id) + ' sfmid ' + sfm_id + ' but could not update or create product, inventory record')
            raise ValidationError(detail={"form": "Purchase saved but could not update or create product, inventory record"})
        headers = self.get_success_headers(serializer.data)
        logger.info(request.user.username + ' created purchase id ' + str(new_purchase.id) + ' sfmid ' + sfm_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        oldStatus = instance.status
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        sfm_id = serializer.validated_data['style'] + '-' + serializer.validated_data['size'] + '-' + \
                 serializer.validated_data['color']
        days_add = 10 if serializer.validated_data['warehouse'].upper() == 'BE' else 5
        arrival_date = serializer.validated_data['orderDate'] + timedelta(days=days_add)
        new_purchase = serializer.save(arrivalDate=arrival_date, sfmId=sfm_id)
        try:
            Utilities.update_inventory(new_purchase, oldStatus)
        except Exception as e:
            print(e)
            logger.error(request.user.username + ' updated purchase id ' + str(new_purchase.id) + ' sfmid ' + sfm_id + ' but some error occurred in updaing inventory')
            raise ValidationError(detail={"form": "Purchase saved but could not update or create product, inventory record"})
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        logger.info(request.user.username + ' updated purchase id ' + str(new_purchase.id) + ' sfmid ' + sfm_id)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        id = instance.id
        sfmId = instance.sfmId
        self.perform_destroy(instance)
        logger.info(
            self.request.user.username + ' deleted purchase id ' + str(id) + ' sfmid ' + sfmId)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['POST'])
    def import_file(self, request, pk=None):
        myfile = request.FILES['purchaseFile']
        if '.csv' in myfile.name:
            data = pd.read_csv(myfile)
            print(data.head())
            errors, msg, failed = Utilities.import_purchases(data)
            print(errors)
        if '.xlsx' in myfile.name:
            data = pd.read_excel(myfile, engine='openpyxl')
            print(data.head())
            errors, msg, failed = Utilities.import_purchases(data)
            print(errors)

        if failed:
            logger.exception(request.user.username + ' Failed to import orders file ' + str(myfile.name) + ", error: " + msg)
        elif len(errors) == 0:
            logger.info(request.user.username + ' Successfully imported purchases file ' + str(myfile.name))
        else:
            errorstring = ','.join(errors)
            # errorstring = errorstring[:200] + '...' if len(errorstring) > 200 else errorstring
            logger.exception(request.user.username + ' Imported purchases file ' + str(myfile.name) + ' with errors ' + errorstring)
        return Response({'errors': errors, 'msg': msg})


