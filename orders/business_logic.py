from .models import Order
from .models import Store
import pandas as pd

class ImportFiles:
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
                order.orderNo = '' if pd.isna(row['orderno']) else str(row['orderno'])
                order.recipientName = '' if pd.isna(row['recipientname']) else str(row['recipientname'])
                order.style = '' if pd.isna(row['style']) else str(row['style'])
                order.size = '' if pd.isna(row['size']) else str(row['size'])
                order.color = '' if pd.isna(row['color']) else str(row['color'])
                order.design = '' if pd.isna(row['design']) else str(row['design'])
                order.processing = 'N'
                order.printed = 'N'
                order.shipped = 'N'
                order.sfmNotes = ''
                order.buyerName = '' if pd.isna(row['buyername']) else str(row['buyername'])
                order.buyerEmail = ''
                order.buyerComments = '' if pd.isna(row['buyercomments']) else str(row['buyercomments'])
                order.giftMessages = '' if pd.isna(row['giftmessage']) else str(row['giftmessage'])
                order.sfmId = str(order .style) + '-' + str(order.size) + '-' + str(order.color)
                order.sku = '' if pd.isna(row['sku']) else str(row['sku'])
                order.shipDate = None
                order.priorityShip = '' if pd.isna(row['priorityshipping']) else str(row['priorityshipping'])
                order.customerPaidShipping = 0
                order.trackingNumber = ''
                order.save()
            except Exception as e:
                errors.append('error row ' + str(index+1) + ': ' + str(e))

        return errors

    def import_shippingDetails(data):

        errors = []
        columnNames = list(data)
        newNames = {col: col.strip().replace(' ', '').lower() for col in columnNames}
        data.rename(columns=newNames, inplace=True)
        data['totalshippingcost'].astype('float64')
        print(newNames)
        print(data.dtypes, len(data.index))
        for index, row in data.iterrows():
            print(row)

            try:
                order = Order.objects.filter(orderNo=str(row['ordernumber'])).first()
                if order is None:
                    raise Exception('order does not exist')

                order.buyerEmail = '' if pd.isna(row['emailaddress']) else str(row['emailaddress'])
                order.customerPaidShipping = None if pd.isna(row['totalshippingcost']) else float(row['totalshippingcost'])
                order.trackingNumber = '' if pd.isna(row['trackingnumber']) else str(row['trackingnumber'])
                order.save()
            except Exception as e:
                errors.append('error row ' + str(index+1) + ': ' + str(e))

        return errors


