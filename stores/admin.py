from django.contrib import admin
from .models import Store
# Register your models here.
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['storeCode', 'storeName', 'zipCode', 'emailAddress', 'city', 'state']
    search_fields = ['storeCode', 'storeName', 'zipCode', 'emailAddress', 'city', 'state']
