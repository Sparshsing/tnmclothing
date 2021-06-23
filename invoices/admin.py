from django.contrib import admin, messages
from django.utils.translation import ngettext
from .logic import generatepdf
from .models import Invoice, InvoiceItems

# Register your models here.
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoiceNo', 'startDate', 'endDate', 'storeName', 'status', 'subTotal', 'total']
    readonly_fields = ('total',)
    search_fields = ['invoiceNo', 'startDate', 'endDate', 'storeName', 'status']
    list_per_page = 50
    actions = ['generate_pdf']

    @admin.action(description='Generate pdf again for these invoices')
    def generate_pdf(self, request, queryset):
        count = 0
        for invoice in queryset:
            generatepdf(invoice.id)
            count += 1
        self.message_user(request, ngettext(
            '%d invoice pdf was successfully generated.',
            '%d invoice pdfs successfully generated.',
            count,
        ) % count, messages.SUCCESS)

@admin.register(InvoiceItems)
class InvoiceItemseAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice', 'shipDate', 'orderDate', 'orderNo', 'customer', 'description', 'amount']
    search_fields = ['id', 'invoice__invoiceNo', 'shipDate', 'orderDate', 'orderNo', 'customer', 'description', 'amount']
    list_per_page = 50
