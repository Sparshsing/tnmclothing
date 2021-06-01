import django_filters

from .models import Order
from stores.models import Store
from inventory.models import Inventory
from .serializers import OrderSerializer
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
import pandas as pd
from .business_logic import ImportFiles

# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = (TokenAuthentication,)
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filterset_fields = ['orderStatus']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user
        if not user.is_superuser and not user.is_staff:
            stores = Store.objects.filter(user=user)
            queryset = Order.objects.filter(store__in=stores)
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
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        inv = Inventory.objects.filter(sfmId=serializer.validated_data['sfmId']).first()

        processing = serializer.validated_data['processing']
        newStatus = serializer.validated_data['orderStatus']

        if serializer.validated_data['shipped'] == 'Y':
            newStatus = 'Shipped'
        elif serializer.validated_data['printed'] == 'Y':
            newStatus = 'Printed'
        else:
            newStatus = ''
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

        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = self.get_object()
        sfmId = serializer.validated_data['sfmId']
        shipped = serializer.validated_data['shipped']
        printed = serializer.validated_data['printed']
        previousProcessing = instance.processing
        processing = serializer.validated_data['processing']
        orderStatus = serializer.validated_data['orderStatus']
        # if status has not been changed by user manually
        #if newStatus in ['', 'Printed', 'Shipped']:
        if shipped == 'Y':
            orderStatus = 'Shipped'
        elif printed == 'Y':
            orderStatus = 'Printed'
        if orderStatus=='' and processing == 'N':
            orderStatus = 'Unfulfilled'
            # otherwise let it be empty, only in frontend show the calculated value.
            # else:
            #     if inv:
            #         newStatus = inv.productAvailability
            #     else:
            #         newStatus = "Invalid Product"
        serializer.save(orderStatus=orderStatus)

        # update inventory

        if processing != previousProcessing:
            inv = Inventory.objects.filter(sfmId=sfmId).first()
            if inv and processing == 'Y':
                inv.inStock = inv.inStock - 1
                inv.save()
            if inv and processing == 'N':
                inv.inStock = inv.inStock + 1
                inv.save()

    @action(detail=False, methods=['POST'])
    def import_ordersfile(self, request, pk=None):

        myfile = request.FILES['ordersFile']

        if'.csv' in myfile.name:
            data = pd.read_csv(myfile)
            # print(data.head())
            errors = ImportFiles.import_orders(data)
            print(errors)
        if '.xlsx' in myfile.name:
            data = pd.read_excel(myfile, engine='openpyxl')
            # print(data.head())
            errors = ImportFiles.import_orders(data)
            print(errors)
        return Response({'errors': errors})

    @action(detail=False, methods=['POST'])
    def import_shippingfile(self, request, pk=None):

        myfile = request.FILES['shippingFile']

        if '.csv' in myfile.name:
            data = pd.read_csv(myfile)
            print(data.head())
            errors = ImportFiles.import_shippingDetails(data)
            print(errors)
        if '.xlsx' in myfile.name:
            data = pd.read_excel(myfile, engine='openpyxl')
            print(data.head())
            errors = ImportFiles.import_shippingDetails(data)
            print(errors)
        return Response({'errors': errors})

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
    queryset = Order.objects.exclude(orderStatus='Shipped')
    authentication_classes = (TokenAuthentication,)






