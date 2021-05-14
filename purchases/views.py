from .models import Purchase
from .serializers import PurchaseSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from .business_logic import ImportFiles
import pandas as pd
from datetime import timedelta

# Create your views here.

class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
    authentication_classes = (TokenAuthentication,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sfm_id = serializer.validated_data['style'] + '-' + serializer.validated_data['size'] + '-' + serializer.validated_data['color']
        days_add = 10 if serializer.validated_data['warehouse'].upper() == 'BE' else 5
        arrival_date = serializer.validated_data['orderDate'] + timedelta(days=days_add)
        serializer.save(arrivalDate=arrival_date, sfmId=sfm_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        sfm_id = serializer.validated_data['style'] + '-' + serializer.validated_data['size'] + '-' + \
                 serializer.validated_data['color']
        days_add = 10 if serializer.validated_data['warehouse'].upper() == 'BE' else 5
        arrival_date = serializer.validated_data['orderDate'] + timedelta(days=days_add)
        serializer.save(arrivalDate=arrival_date, sfmId=sfm_id)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def import_file(self, request, pk=None):
        myfile = request.FILES['purchaseFile']
        if '.csv' in myfile.name:
            data = pd.read_csv(myfile)
            print(data.head())
            errors = ImportFiles.import_purchases(data)
            print(errors)
        if '.xlsx' in myfile.name:
            data = pd.read_excel(myfile, engine='openpyxl')
            print(data.head())
            errors = ImportFiles.import_purchases(data)
            print(errors)
        return Response({'errors': errors})


