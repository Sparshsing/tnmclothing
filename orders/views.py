
import django_filters

from .models import Order
from stores.models import Store
from inventory.models import Inventory
from .serializers import OrderSerializer
from rest_framework import viewsets, status
from rest_framework import pagination, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from django.db.models import F
import datetime
import pandas as pd
from .business_logic import ImportFiles
import logging

# Get an instance of a logger
logger = logging.getLogger('db')

class OrdersPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = (TokenAuthentication,)
    pagination_class = OrdersPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['style', 'size', 'color', 'orderStatus', 'orderNo', 'store__storeName', 'recipientName', 'design']

    def list(self, request, *args, **kwargs):
        sorted_orders_qs = Order.objects.order_by(F('shipDate').desc(nulls_first=True), 'store__storeName', 'recipientName')
        queryset = self.filter_queryset(sorted_orders_qs)
        user = request.user
        if not user.is_superuser and not user.is_staff:
            stores = Store.objects.filter(user=user)
            queryset = queryset.filter(store__in=stores)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(request.user.username + ' created Order Id ' + str(serializer.data['orderId']))
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        inv = Inventory.objects.filter(sfmId=serializer.validated_data['sfmId']).first()

        processing = serializer.validated_data['processing']
        newStatus = 'Unfulfilled'

        if processing == 'Y':
            newStatus = 'Processed'
        if serializer.validated_data['printed'] == 'Y':
            newStatus = 'Printed'
        if serializer.validated_data['shipped'] == 'Y':
            newStatus = 'Shipped'
        # otherwise let it be empty, only in frontend show the calculated value.
        # else:
        #     if inv:
        #         newStatus = inv.productAvailability
        #     else:
        #         newStatus = "Invalid Product"
        serializer.save(orderStatus=newStatus)
        if inv:
            if processing == 'Y':
                inv.inStock = inv.inStock - 1
                inv.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        logger.info(request.user.username + ' updated Order Id ' + str(instance.orderId))
        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = self.get_object()
        oldStatus =instance.orderStatus
        sfmId = serializer.validated_data['sfmId']
        shipped = serializer.validated_data['shipped']
        printed = serializer.validated_data['printed']
        previousProcessing = instance.processing
        processing = serializer.validated_data['processing']
        orderStatus = serializer.validated_data['orderStatus']
        # if status has not been changed by user manually
        #if newStatus in ['', 'Printed', 'Shipped']:
        if orderStatus != 'Cancelled':
            orderStatus = 'Unfulfilled'
            if processing == 'Y':
                orderStatus = 'Processed'
            if printed == 'Y':
                orderStatus = 'Printed'
            if shipped == 'Y':
                orderStatus = 'Shipped'



        # otherwise let it be empty, only in frontend show the calculated value.
        # else:
        #     if inv:
        #         newStatus = inv.productAvailability
        #     else:
        #         newStatus = "Invalid Product"
        # if status changed to shipped
        if orderStatus!=oldStatus and orderStatus=="Shipped" and serializer.validated_data['shipDate'] is None:
            serializer.save(orderStatus=orderStatus, shipDate=datetime.datetime.utcnow())
        # if status changed from shipped to something else
        elif orderStatus!=oldStatus and oldStatus=="Shipped":
            serializer.save(orderStatus=orderStatus, shipDate=None)
        else:
            serializer.save(orderStatus=orderStatus)

        if orderStatus != oldStatus:
            logger.info(self.request.user.username + ' updated order status to ' + orderStatus)
        # update inventory

        if processing != previousProcessing:
            inv = Inventory.objects.filter(sfmId=sfmId).first()
            if inv and processing == 'Y':
                inv.inStock = inv.inStock - 1
                inv.save()
            if inv and processing == 'N':
                inv.inStock = inv.inStock + 1
                inv.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        id = instance.orderId
        self.perform_destroy(instance)
        logger.info(request.user.username + ' deleted Order Id ' + str(id))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['POST'])
    def import_ordersfile(self, request, pk=None):
        myfile = request.FILES['ordersFile']

        if'.csv' in myfile.name:
            data = pd.read_csv(myfile)
            # print(data.head())
            errors, msg, failed = ImportFiles.import_orders(data)
            print(errors)
        if '.xlsx' in myfile.name:
            data = pd.read_excel(myfile, engine='openpyxl')
            # print(data.head())
            errors, msg, failed = ImportFiles.import_orders(data)
            print(errors)

        if failed:
            logger.exception(request.user.username + ' Failed to import orders file ' + str(myfile.name) + ", error: " + msg)
        elif len(errors) == 0:
            logger.info(request.user.username + ' imported orders file ' + str(myfile.name) + ' Successfully')
        else:
            errorstring = ','.join(errors)
            # errorstring = errorstring[:200] + '...' if len(errorstring) > 200 else errorstring
            logger.exception(
                request.user.username + ' Imported orders file ' + str(myfile.name) + ' with errors ' + errorstring)
        return Response({'errors': errors, 'msg': msg})

    @action(detail=False, methods=['POST'])
    def import_shippingfile(self, request, pk=None):

        myfile = request.FILES['shippingFile']

        if '.csv' in myfile.name:
            data = pd.read_csv(myfile)
            print(data.head())
            errors, msg, failed = ImportFiles.import_shippingDetails(data)
            print(errors)
        if '.xlsx' in myfile.name:
            data = pd.read_excel(myfile, engine='openpyxl')
            print(data.head())
            errors, msg, failed = ImportFiles.import_shippingDetails(data)
            print(errors)

        if failed:
            logger.exception(request.user.username + ' Failed to import shipping file ' + str(myfile.name) + ", error: " + msg)
        elif len(errors) == 0:
            logger.info(request.user.username + ' Imported shipping file ' + str(myfile.name) + ' Successfully')
        else:
            errorstring = ','.join(errors)
            # errorstring = errorstring[:500] + '...' if len(errorstring) > 500 else errorstring
            logger.exception(request.user.username + ' imported shipping file ' + str(myfile.name) + ' with errors ' + errorstring)
        return Response({'errors': errors, 'msg': msg})

    @action(detail=False, methods=['POST'])
    def get_overview(self, request, pk=None):
        print(request.data, type(request.data))
        store = request.data['store']
        startDate = request.data['startDate']
        endDate = request.data['endDate']
        orders = None
        if store == '':
            raise serializers.ValidationError({"store": "store cannot be empty"})
        if store == 'All':
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(store=store)
        print(orders)
        if startDate=='' and endDate!='':
            orders = orders.filter(saleDate__lte=endDate)
        elif endDate=='' and startDate!='':
            orders = orders.filter(saleDate__gte=startDate)
        elif startDate!='' and endDate!='':
            orders = orders.filter(saleDate__gte=startDate, saleDate__lte=endDate)
        result = {}
        result['total'] = orders.count()
        result['unfulfilled'] = orders.filter(orderStatus='Unfulfilled').count()
        result['onhold'] = orders.filter(orderStatus='On Hold').count()
        result['fulfilled'] = orders.filter(orderStatus__in=['Printed', 'Shipped']).count()
        outofstock = 0
        for order in orders:
            if order.orderStatus=='':
                inv = Inventory.objects.filter(sfmId=order.sfmId).first()
                if inv and inv.productAvailability=='Out Of Stock':
                    outofstock +=1
        result['outofstock'] = outofstock

        result['storecount'] = Store.objects.all().count()

        return Response(result)


class PrintingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.exclude(orderStatus='Cancelled').exclude(orderStatus='Shipped').order_by('-orderId')
    authentication_classes = (TokenAuthentication,)






