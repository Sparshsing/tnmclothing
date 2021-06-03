from django.contrib import admin
from .models import Invoice

# Register your models here.
# @admin.register(Invoice)
# class InvoiceAdmin(admin.ModelAdmin):
#     list_display = ['orderId', 'orderNo', 'orderStatus', 'store', 'recipientName', 'style', 'size', 'color']
#     search_fields = ['orderId', 'orderNo', 'orderStatus', 'store__storeName', 'recipientName', 'style', 'size', 'color']
