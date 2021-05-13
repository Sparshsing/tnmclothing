from .models import Order
from .models import Store
import pandas as pd
from datetime import date
class ImportOrders:
    @staticmethod
    def import_orders(data):
        cols = {'store': 'STORE', 'saleDate': 'SALE DATE', 'orderNo': 'ORDER NO',
                'recipientName': 'RECIPIENT NAME', 'style': 'STYLE', 'size': 'SIZE', 'color': 'COLOR',
                'design': 'DESIGN', 'buyerName': 'BUYER NAME',
                'buyerComments': 'BUYER COMMENTS', 'giftMessages': 'GIFT MESSAGE'}
        errors = []
        columnNames = list(data)
        newNames = {col: col.strip().replace(' ', '').lower() for col in columnNames}
        data.rename(columns=newNames, inplace=True)
        print(newNames)
        print(data.dtypes)
        for index, row in data.iterrows():
            print(row)

            try:
                order = Order()
                store = Store.objects.get(storeName=str(row['store']))
                order.store = store
                order.orderStatus = ''
                order.saleDate = None if pd.isna(row['saledate']) else row['saledate'].date()
                order.orderNo = str(row['orderno'])
                order.recipientName = str(row['recipientname'])
                order.style = str(row['style'])
                order.size = str(row['size'])
                order.color = str(row['color'])
                order.design = str(row['design'])
                order.processing = 'N'
                order.printed = 'N'
                order.shipped = 'N'
                order.sfmNotes = ''
                order.buyerName = str(row['buyername'])
                order.buyerEmail = ''
                order.buyerComments = str(row['buyercomments'])
                order.giftMessages = str(row['giftmessage'])
                order.sfmId = str(row['style']) + '-' + str(row['size']) + '-' + str(row['color'])
                order.sku = str(row['sku'])
                order.shipDate = None
                order.priorityShip = str(row['priorityshipping'])
                order.customerPaidShipping = 0
                order.trackingNumber = ''
                order.save()
            except Exception as e:
                errors.append('error row ' + str(index+1) + ': ' + str(e))

        return errors


