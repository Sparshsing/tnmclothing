from django.contrib import admin
from .models import Product
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sfmId', 'style', 'size', 'color', 'price']
    search_fields = ['sfmId', 'style', 'size', 'color']