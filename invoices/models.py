from django.db import models

# Create your models here.
class Invoice(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    storeName = models.CharField(max_length=50)
    invoiceNo = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10)
    notes = models.CharField(max_length=500)
    subTotal = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    taxrate = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=5, decimal_places=2)

class InvoiceItems(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='invoiceItem', on_delete=models.CASCADE)
    shipDate = models.DateField()
    orderDate = models.DateField()
    orderNo = models.CharField(max_length=20)
    customer = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=5, decimal_places=2)


