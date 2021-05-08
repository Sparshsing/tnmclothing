from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Purchase(models.Model):
    status = models.CharField(max_length=10)
    style = models.CharField(max_length=30)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=25)
    company = models.CharField(max_length=20, blank=True)
    warehouse = models.CharField(max_length=20)
    ordered = models.IntegerField(validators=[MinValueValidator, MaxValueValidator])
    orderDate = models.DateField()
    arrivalDate = models.DateField()
    sfmId = models.CharField(max_length=50)

    def __str__(self):
        return self.sfmId




