from .models import Order
from stores.models import Store
from inventory.models import Inventory
from datetime import datetime
import pandas as pd
import logging


# Get an instance of a logger
logger = logging.getLogger('db')

def convert_date(val):
    """
    Convert to datetime object if string
    """

    if isinstance(val, str):
        try:
            newval = datetime.strptime(str(val), '%m/%d')
        except ValueError as err:
            newval = datetime.strptime(str(val), '%m/%d/%Y')
        newval = newval.replace(year=datetime.now().year)

        return newval

    return val

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
        # print(newNames)
        print(data.dtypes)
        msg = ''
        failed = False

        columns_needed = {'store', 'saledate', 'orderno', 'recipientname', 'style', 'size', 'color', 'design', 'buyername', 'buyercomments', 'giftmessage', 'sku', 'priorityshipping'}
        columns_available = set(newNames.values())
        missing = columns_needed.difference(columns_available)

        if len(missing) > 0:
            msg = "Import failed. Please make sure these columns are present in import file: 'store', 'sale date', 'order no', 'recipient name', 'style', 'size', 'color', 'design', 'buyer name', 'buyer comments', 'gift message', 'sku', 'priority shipping'"
            failed = True
            return errors, msg, failed

        try:
            data['saledate'] = data['saledate'].apply(convert_date)
            data['saledate'] = data['saledate'].astype('datetime64')
        except Exception as err:
            msg = 'Import Failed. Please make sure Sale Date column has dates as mm/dd/yyyy or mm/dd or empty values'
            failed = True
            logger.exception('error reading sale date column')
            return errors, msg, failed

        for index, row in data.iterrows():
            # print(row)

            try:
                order = Order()
                store = Store.objects.get(storeName=str(row['store']).strip())
                order.store = store
                order.orderStatus = 'Unfulfilled'
                order.saleDate = None if pd.isna(row['saledate']) else row['saledate'].date()
                order.orderNo = '' if pd.isna(row['orderno']) else str(row['orderno']).strip()
                order.recipientName = '' if pd.isna(row['recipientname']) else str(row['recipientname']).strip()
                order.style = '' if pd.isna(row['style']) else str(row['style']).strip()
                order.size = '' if pd.isna(row['size']) else str(row['size']).strip()
                order.color = '' if pd.isna(row['color']) else str(row['color']).strip()
                order.design = '' if pd.isna(row['design']) else str(row['design']).strip()
                order.processing = 'N'
                order.printed = 'N'
                order.shipped = 'N'
                order.sfmNotes = ''
                order.buyerName = '' if pd.isna(row['buyername']) else str(row['buyername']).strip()
                order.buyerEmail = ''
                order.buyerComments = '' if pd.isna(row['buyercomments']) else str(row['buyercomments']).strip()
                order.giftMessages = '' if pd.isna(row['giftmessage']) else str(row['giftmessage']).strip()
                order.sfmId = str(order .style) + '-' + str(order.size) + '-' + str(order.color)
                order.sku = '' if pd.isna(row['sku']) else str(row['sku']).strip()
                order.shipDate = None
                order.priorityShip = '' if pd.isna(row['priorityshipping']) else str(row['priorityshipping']).strip()
                order.customerPaidShipping = 0
                order.trackingNumber = ''
                order.save()
                # if order.processing == 'Y':
                #     inv = Inventory.objects.filter(sfmId=order['sfmId']).first()
                #     if inv:
                #         inv.inStock = inv.inStock - 1
                #         inv.save()

            except Exception as e:
                errors.append('error row ' + str(index+2) + ': ' + str(e))
        if len(errors) > 0:
            msg = 'Some records were not imported'
        else:
            msg = 'Successfully imported all records'
        return errors, msg, failed

    def import_shippingDetails(data):

        errors = []
        msg = ''
        failed = False
        columnNames = list(data)
        newNames = {col: col.strip().replace(' ', '').lower() for col in columnNames}
        data.rename(columns=newNames, inplace=True)
        columns_needed = {'store', 'postagecost', 'emailaddress', 'trackingnumber', 'ordernumber'}
        columns_available = set(newNames.values())
        missing = columns_needed.difference(columns_available)
        if len(missing) > 0:
            msg = 'Import failed. Please make sure these columns are present in import file: Store, Order Number, Email Address, Postage Cost, Tracking Number'
            failed = True
            return errors, msg, failed
        try:
            data['postagecost'] = data['postagecost'].astype('float64')
        except Exception as err:
            msg = 'Import failed. Please make sure cost column has decimal numbers or empty values'
            failed = True
            return errors, msg, failed
        # print(newNames)
        for index, row in data.iterrows():
            # print(row)

            try:
                orders = Order.objects.filter(orderNo=str(row['ordernumber']).strip())
                if orders.first() is None:
                    raise Exception('order does not exist')
                for order in orders:
                    order.buyerEmail = '' if pd.isna(row['emailaddress']) else str(row['emailaddress']).strip()
                    order.customerPaidShipping = None if pd.isna(row['postagecost']) else float(row['postagecost'])
                    order.trackingNumber = '' if pd.isna(row['trackingnumber']) else str(row['trackingnumber']).strip()
                    # order.orderStatus = 'Shipped'
                    # order.shipDate = datetime.utcnow()
                    order.save()
            except Exception as e:
                errors.append('error row ' + str(index+2) + ': ' + str(e))
        if len(errors) > 0:
            msg = 'Some records were not imported'
        else:
            msg = 'Successfully imported all records'
        return errors, msg, failed


