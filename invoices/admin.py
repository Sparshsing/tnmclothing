from django.contrib import admin
from .models import Invoice, InvoiceItems

# Register your models here.
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoiceNo', 'startDate', 'endDate', 'storeName', 'status', 'subTotal', 'total']
    readonly_fields = ('total',)
    search_fields = ['invoiceNo', 'startDate', 'endDate', 'storeName', 'status']
    list_per_page = 50

@admin.register(InvoiceItems)
class InvoiceItemseAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice', 'shipDate', 'orderDate', 'orderNo', 'customer', 'description', 'amount']
    search_fields = ['id', 'invoice__invoiceNo', 'shipDate', 'orderDate', 'orderNo', 'customer', 'description', 'amount']
    list_per_page = 50
