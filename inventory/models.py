from django.db import models
from purchases.models import Purchase
from orders.models import Order

# Create your models here.

class Inventory(models.Model):
    sfmId = models.CharField(max_length=50, primary_key=True)
    style = models.CharField(max_length=30)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=25)
    inStock = models.IntegerField()
    arrivalDate = models.DateField()
    minimum = models.IntegerField()
    maximum = models.IntegerField()

    @property
    def inTransit(self):
        res = Purchase.objects.filter(sfmId=self.sfmId, status__icontains='transit').first()
        if res:
            return res.ordered
        else:
            return 0

    @property
    def unfulfilledCount(self):
        return Order.objects.filter(sfmId=self.sfmId, processing__icontains='N').count()

    @property
    def productAvailability(self):
        if self.inStock > 0:
            if self.unfulfilledCount > self.inStock:
                return "Short"
            else:
                return "Good"
        elif self.inTransit > 0:
            return "Restock on " + self.arrivalDate
        else:
            return "Out Of Stock"

    @property
    def trueCount(self):
        return self.inStock + self.inTransit - self.unfulfilledCount

    @property
    def shortCount(self):
        return self.maximum - self.trueCount

    @property
    def needToPurchase(self):
        if self.trueCount < self.minimum:
            return self.maximum - self.trueCount
        return 0

    def __str__(self):
        return self.sfmId




