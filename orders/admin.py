from django.contrib import admin
from .models import Order

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['orderId', 'orderNo', 'orderStatus', 'store', 'recipientName', 'style', 'size', 'color']
    search_fields = ['orderId', 'orderNo', 'orderStatus', 'store__storeName', 'recipientName', 'style', 'size', 'color']
    list_per_page = 50