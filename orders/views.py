from .models import Order
from inventory.models import Inventory
from .serializers import OrderSerializer
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
import pandas as pd
from .business_logic import ImportFiles

# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = (TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        inv = Inventory.objects.filter(sfmId=serializer.validated_data['sfmId']).first()

        processing = serializer.validated_data['processing']
        newStatus = serializer.validated_data['status']
        if newStatus == '':
            if serializer.validated_data['shipped'] == 'Y':
                newStatus = 'Shipped'
            elif serializer.validated_data['printed'] == 'Y':
                newStatus = 'Printed'
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
        inv = Inventory.objects.filter(sfmId=serializer.validated_data['sfmId']).first()
        instance = self.get_object()
        previousProcessing = instance.processing


        newStatus = serializer.validated_data['status']
        # if status has not been changed by user manually
        if newStatus == instance.orderStatus:
            if serializer.validated_data['shipped'] == 'Y':
                newStatus = 'Shipped'
            elif serializer.validated_data['printed'] == 'Y':
                newStatus = 'Printed'
            # otherwise let it be empty, only in frontend show the calculated value.
            # else:
            #     if inv:
            #         newStatus = inv.productAvailability
            #     else:
            #         newStatus = "Invalid Product"
        serializer.save(orderStatus=newStatus)
        serializer.save()

        # update inventory
        if inv:
            if previousProcessing == 'N' and serializer.validated_data['processing'] == 'Y':
                inv.inStock = inv.inStock - 1
                inv.save()
            if previousProcessing and serializer.validated_data['processing'] == 'N':
                inv.inStock = inv.inStock + 1
                inv.save()

    @action(detail=False, methods=['POST'])
    def import_ordersfile(self, request, pk=None):

        myfile = request.FILES['ordersFile']

        if'.csv' in myfile.name:
            data = pd.read_csv(myfile)
            print(data.head())
            errors = ImportFiles.import_orders(data)
            print(errors)
        if '.xlsx' in myfile.name:
            data = pd.read_excel(myfile, engine='openpyxl')
            print(data.head())
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




