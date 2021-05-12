from django.db import models
from stores.models import Store

# Create your models here.

class Order(models.Model):
    orderId = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, related_name='order', null=True, on_delete=models.SET_NULL)
    orderStatus = models.CharField(max_length=15, blank=True)
    saleDate = models.DateField(null=True)
    orderNo = models.CharField(max_length=20)
    recipientName = models.CharField(max_length=50)
    style = models.CharField(max_length=30)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=25)
    design = models.CharField(max_length=50, blank=True)
    processing = models.CharField(max_length=1)
    printed = models.CharField(max_length=1, blank=True)
    shipped = models.CharField(max_length=1)
    sfmNotes = models.CharField(max_length=5000, blank=True)
    buyerName = models.CharField(max_length=50, blank=True)
    buyerEmail = models.CharField(max_length=50, blank=True)
    buyerComments = models.CharField(max_length=5000, blank=True)
    giftMessages = models.CharField(max_length=5000, blank=True)
    sfmId = models.CharField(max_length=50)
    sku = models.CharField(max_length=20, blank=True)
    shipDate = models.DateTimeField(null=True, blank=True)
    priorityShip = models.CharField(max_length=50, blank=True)
    customerPaidShipping = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    trackingNumber = models.CharField(max_length=30, blank=True)

    @property
    def storeName(self):
        return self.store.storeName

    @property
    def orderCount(self):
        return Order.objects.filter(orderNo=self.orderNo).count()

    def __str__(self):
        return self.orderNo




