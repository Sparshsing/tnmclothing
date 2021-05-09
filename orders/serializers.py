from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    # orderCount = serializers.SerializerMethodField()
    # sfmId = serializers.SerializerMethodField()
    # productAvailability = serializers.SerializerMethodField()
    # orderStatus = serializers.SerializerMethodField()
    # style = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('orderId', 'store', 'storeName', 'orderStatus', 'saleDate', 'orderNo', 'orderCount', 'recipientName', 'style', 'size', 'color', 'design', 'processing', 'printed', 'shipped', 'sfmNotes', 'buyerName', 'buyerEmail', 'buyerComments', 'giftMessages', 'sfmId', 'sku', 'shipDate', 'priorityShip', 'customerPaidShipping', 'trackingNumber', 'productAvailability')

    # def get_sfmId(self, order):
    #     return order.style + '-' + order.size + '-' + order.color

    # def get_orderCount(self, order):
    #     return Order.objects.filter(orderNo=order.orderNo).count()

    # def get_productAvailability(self, order):
    #     return 'dummy'
    #
    # def get_orderStatus(self, order):
    #     if order.shipped.upper() == 'Y':
    #         return 'Shipped'
    #     if order.printed.upper() == 'Y':
    #         return 'Printed'
    #     return self.productAvailability
