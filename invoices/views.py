from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, pagination, filters
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from datetime import datetime
from .models import Invoice, InvoiceItems
from .logic import create_invoices, generatepdf
from stores.models import Store
from .serializers import InvoiceSerializer, InvoiceDetailsSerializer, ReceiptUploadSerializer
import logging


# Get an instance of a logger
logger = logging.getLogger('db')

class InvoicePagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

def invoice_pdf_view(request, id, *args):
    invoice = get_object_or_404(Invoice, id=id)
    items = InvoiceItems.objects.filter(invoice=invoice)
    items = [item for item in items]
    itemcount = len([item for item in items if item.description != 'Shipping'])
    ordercount = len({item.orderNo for item in items})
    store = Store.objects.filter(storeCode=invoice.store.storeCode).first()
    afterdiscount = invoice.subTotal - invoice.discount
    taxamount = round(afterdiscount * invoice.taxrate * Decimal(0.01), 2)
    logourl = settings.BACKEND_URL + "/static/logosfm2.jpg"
    context = {"invoice": invoice, "items": items, "store": store, "itemcount": itemcount, "ordercount": ordercount,
               "afterdiscount": afterdiscount, "taxamount": taxamount, "logourl": logourl}

    # generatepdf(id)
    return render(request, 'invoiceDetails.html', context)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = InvoicePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['invoiceNo', 'storeName', 'status']

    def list(self, request, *args, **kwargs):

        sorted_queryset = Invoice.objects.all().order_by('-id')
        queryset = self.filter_queryset(sorted_queryset)
        if not request.user.is_superuser:
            stores = Store.objects.filter(user=request.user.id)
            storenames = [s.storeName for s in stores]
            queryset = queryset.filter(storeName__in=storenames)
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
    def generate_invoices(self, request, pk=None):
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

    @action(detail=True, methods=['POST'])
    def upload_receipt(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ReceiptUploadSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(self.request.user.username + ' uploaded receipt ' + instance.invoiceNo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            logger.exception(self.request.user.username + ' Failed to upload receipt ' + instance.invoiceNo)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



