from django.db import models

# Create your models here.

class Product(models.Model):
    sfmId = models.CharField(max_length=50, primary_key=True)
    style = models.CharField(max_length=30)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=25)
    sku = models.CharField(max_length=20, unique=True, blank=True, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    amountInStock = models.CharField(max_length=50)

    def __str__(self):
        return self.sfmId




