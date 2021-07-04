from rest_framework import serializers
from .models import Invoice, InvoiceItems
from stores.serializers import StoreSerializer

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('id', 'startDate', 'endDate', 'store', 'storeName', 'invoiceNo', 'status', 'notes', 'subTotal', 'discount', 'taxrate', 'total', 'attachment', 'receipt')
        read_only_fields = ['attachment', 'receipt', 'id', 'startDate', 'endDate', 'store', 'storeName', 'invoiceNo']

class ReceiptUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['receipt']

    # uncomment if you want to delete existing receipt of this invoice
    # def save(self, *args, **kwargs):
    #     if self.instance.receipt:
    #         self.instance.receipt.delete()
    #     return super().save(*args, **kwargs)

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




