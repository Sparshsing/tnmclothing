from rest_framework import serializers
from .models import Order
from inventory.models import Inventory

class OrderSerializer(serializers.ModelSerializer):
    # orderCount = serializers.SerializerMethodField()
    # sfmId = serializers.SerializerMethodField()
    # productAvailability = serializers.SerializerMethodField()
    # orderStatus = serializers.SerializerMethodField()
    # style = serializers.SerializerMethodField()
    productAvailability = serializers.SerializerMethodField()
    displayStatus = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('orderId', 'store', 'storeName', 'orderStatus', 'displayStatus', 'saleDate', 'orderNo', 'orderCount', 'recipientName', 'style', 'size', 'color', 'design', 'processing', 'printed', 'shipped', 'sfmNotes', 'buyerName', 'buyerEmail', 'buyerComments', 'giftMessages', 'sfmId', 'sku', 'shipDate', 'priorityShip', 'customerPaidShipping', 'trackingNumber', 'productAvailability')
        read_only_fields = ['orderId', 'productAvailability']

    def get_productAvailability(self, order):
        res = Inventory.objects.filter(sfmId=order.sfmId).first()
        if res:
            return res.productAvailability
        else:
            return "Unknown"

    def get_displayStatus(self, order):
        status = order.orderStatus
        if status=='':
            res = Inventory.objects.filter(sfmId=order.sfmId).first()
            if res:
                return res.productAvailability
            else:
                return "Unknown"
        else:
            return status

    # def get_sfmId(self, order):
    #     return order.style + '-' + order.size + '-' + order.color

    # def get_orderCount(self, order):
    #     return Order.objects.filter(orderNo=order.orderNo).count()


    #
    # def get_orderStatus(self, order):
    #     if order.shipped.upper() == 'Y':
    #         return 'Shipped'
    #     if order.printed.upper() == 'Y':
    #         return 'Printed'
    #     return self.productAvailability
