from django.contrib import admin
from .models import Inventory
# Register your models here.

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['sfmId', 'style', 'size', 'color', 'inStock']
    search_fields = ['sfmId', 'style', 'size', 'color', 'inStock']
