from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from datetime import datetime
from .models import Invoice, InvoiceItems
from .logic import create_invoices
from stores.models import Store
from .serializers import InvoiceSerializer, InvoiceDetailsSerializer
import logging

# Get an instance of a logger
logger = logging.getLogger('db')


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    authentication_classes = (TokenAuthentication,)

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset().order_by('-id')
        if not request.user.is_superuser:
            stores = Store.objects.filter(user=request.user.id)
            storenames = [s.storeName for s in stores]
            queryset = self.get_queryset().filter(storeName__in=storenames)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = InvoiceDetailsSerializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
        logger.info(self.request.user.username + ' updated Invoice ' + str(serializer.data['invoiceNo']))

    @action(detail=False, methods=['POST'])
    def generate_invoices(request):
        errors = []
        startDate = None
        endDate = None
        try:
            startDate = datetime.strptime(request.data['startDate'], '%Y-%m-%d').date()
            endDate = datetime.strptime(request.data['endDate'], '%Y-%m-%d').date()
        except Exception as e:
            return Response({'startDate': 'required fields'}, status=status.HTTP_400_BAD_REQUEST)
        count = create_invoices(startDate, endDate)
        return Response({'errors': errors, 'count': count})
