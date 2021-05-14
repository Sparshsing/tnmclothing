from .models import Order
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




