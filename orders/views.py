from .models import Order
from .serializers import OrderSerializer
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
import pandas as pd
from .business_logic import ImportOrders

# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['POST'])
    def import_file(self, request, pk=None):
        #file_serializer = FileSerializer(data=request.data)
        #x = file_serializer.ordersFile
        #print(x)
        myfile = request.FILES['ordersFile']
        # with open('name.txt', 'w') as destination:
        #     for chunk in myfile.chunks():
        #         destination.write(chunk)
        #     print(destination)
        # for line in myfile:
        #     print(line)
        if'.csv' in myfile.name:
            data = pd.read_csv(myfile)
            print(data.head())
        if '.xlsx' in myfile.name:
            data = pd.read_excel(myfile, engine='openpyxl')
            print(data.head())
            errors = ImportOrders.import_orders(data)
            print(errors)
        return Response({'errors': errors})




