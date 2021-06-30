from .models import Inventory
from .serializers import InventorySerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import pandas as pd
from rest_framework.authentication import TokenAuthentication
from .logic import Utilities

import logging

# Get an instance of a logger
logger = logging.getLogger('db')

# Create your views here.

class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all().order_by('sfmId')
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['POST'])
    def import_file(self, request, pk=None):

        myfile = request.FILES['inventoryFile']

        if '.csv' in myfile.name:
            data = pd.read_csv(myfile)
            print(data.head())
            errors, msg, failed = Utilities.import_inventory(data)
            print(errors)
        if '.xlsx' in myfile.name:
            data = pd.read_excel(myfile, engine='openpyxl')
            print(data.head())
            errors, msg, failed = Utilities.import_inventory(data)
            print(errors)

        if failed:
            logger.exception(request.user.username + ' Failed to import inventory file ' + str(myfile.name) + ", error: " + msg)
        elif len(errors) == 0:
            logger.info(request.user.username + ' Successfully imported inventory file ' + str(myfile.name))
        else:
            errorstring = ','.join(errors)
            # errorstring = errorstring[:200] + '...' if len(errorstring) > 200 else errorstring
            logger.exception(
                request.user.username + ' imported inventory file ' + str(myfile.name) + ' with errors ' + errorstring)

        return Response({'errors': errors, 'msg': msg})

