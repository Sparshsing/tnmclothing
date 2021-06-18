from django.db import models
from stores.models import Store
from decimal import Decimal

# Create your models here.
class Invoice(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    storeName = models.CharField(max_length=50)
    invoiceNo = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10)
    notes = models.CharField(max_length=500)
    subTotal = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.DecimalField(max_digits=9, decimal_places=2)
    taxrate = models.DecimalField(max_digits=4, decimal_places=2)
    attachment = models.FileField(upload_to='invoicepdfs/', null=True)

    @property
    def total(self):
        totalafterdisc = self.subTotal - self.discount
        totamount = (self.taxrate * Decimal(0.01) + Decimal(1)) * totalafterdisc
        return round(totamount, 2)

    def __str__(self):
        return self.invoiceNo

class InvoiceItems(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    shipDate = models.DateField()
    orderDate = models.DateField()
    orderNo = models.CharField(max_length=20)
    customer = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.invoice.invoiceNo + " item"




