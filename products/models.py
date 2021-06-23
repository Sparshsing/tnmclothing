from django.db import models
from inventory.models import Inventory

# Create your models here.

class Product(models.Model):
    sfmId = models.CharField(max_length=50, unique=True)
    style = models.CharField(max_length=30)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=25)
    sku = models.CharField(max_length=20, unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    @property
    def amountInStock(self):
        inv = Inventory.objects.filter(sfmId=self.sfmId).first()
        if inv is None:
            return 0
        else:
            return inv.inStock

    def __str__(self):
        return self.sfmId




