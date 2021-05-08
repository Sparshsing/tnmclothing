from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class Store(models.Model):
    storeName = models.CharField(max_length=50, unique=True)
    storeCode = models.CharField(max_length=4, primary_key=True)
    emailAddress = models.EmailField(max_length=50)
    addressLine1 = models.CharField(max_length=50)
    addressLine2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipCode = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99999)])

    def __str__(self):
        return self.storeName
