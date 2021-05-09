from django.db import models
from stores.models import Store

# Create your models here.

class Order(models.Model):
    orderId = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, related_name='order', null=True, on_delete=models.SET_NULL)
    orderStatus = models.CharField(max_length=15)
    saleDate = models.DateField()
    orderNo = models.CharField(max_length=20)
    recipientName = models.CharField(max_length=50)
    style = models.CharField(max_length=30)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=25)
    design = models.CharField(max_length=50)
    processing = models.CharField(max_length=1)
    printed = models.CharField(max_length=1)
    shipped = models.CharField(max_length=1)
    sfmNotes = models.CharField(max_length=5000)
    buyerName = models.CharField(max_length=50)
    buyerEmail = models.CharField(max_length=50)
    buyerComments = models.CharField(max_length=5000)
    giftMessages = models.CharField(max_length=5000)
    sfmId = models.CharField(max_length=50)
    sku = models.CharField(max_length=20)
    shipDate = models.DateTimeField(null=True)
    priorityShip = models.CharField(max_length=50)
    customerPaidShipping = models.DecimalField(max_digits=5, decimal_places=2)
    trackingNumber = models.CharField(max_length=30)
    productAvailability = models.CharField(max_length=20)

    @property
    def storeName(self):
        return self.store.storeName

    @property
    def orderCount(self):
        return Order.objects.filter(orderNo=self.orderNo).count()

    def __str__(self):
        return self.orderNo




