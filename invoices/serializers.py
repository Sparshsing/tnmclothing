from rest_framework import serializers
from .models import Invoice, InvoiceItems
from stores.serializers import StoreSerializer

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItems
        fields = '__all__'

class InvoiceDetailsSerializer(serializers.ModelSerializer):
    items = InvoiceItemsSerializer(many=True)
    store = StoreSerializer(many=False)

    class Meta:
        model = Invoice
        fields = ['startDate', 'endDate', 'storeName', 'invoiceNo', 'status', 'notes', 'subTotal', 'discount', 'taxrate', 'items', 'store', 'total']




