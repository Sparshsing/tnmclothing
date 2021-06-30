from .models import Purchase
import pandas as pd
from datetime import timedelta, date, datetime
from products.models import Product
from inventory.models import Inventory


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
        print(newval, type(newval))
        return newval

    return val

class Utilities:
    @staticmethod
    def update_inventory(purchase, oldStatus=''):

        Utilities.create_product_inventory(purchase)

        inventory = Inventory.objects.filter(sfmId=purchase.sfmId).first()
        if purchase.status == 'Received':
            inventory.inStock = inventory.inStock + purchase.ordered
            inventory.arrivalDate = None

        if purchase.status != 'Received':
            inventory.arrivalDate = purchase.arrivalDate
            if oldStatus == 'Received':
                inventory.inStock = inventory.inStock - purchase.ordered
        inventory.save()

    @staticmethod
    def create_product_inventory(purchase):
        prod = Product.objects.filter(sfmId=purchase.sfmId).first()
        if prod is None:
            new_Product = Product(sfmId=purchase.sfmId, style=purchase.style, size=purchase.size, color=purchase.color, price=0.0)
            new_Product.save()
        inv = Inventory.objects.filter(sfmId=purchase.sfmId).first()
        # if inventory exists return else create inventory
        if inv is None:
            new_inventory = Inventory(sfmId=purchase.sfmId, style=purchase.style, size=purchase.size, color=purchase.color, inStock=0.0,
                                      arrivalDate=date.today(), minimum=0, maximum=100)
            new_inventory.save()

    @staticmethod
    def import_purchases(data):
        errors = []
        columnNames = list(data)
        # renaming columns to avoid problems with Case and spaces
        newNames = {col: col.strip().replace(' ', '').lower() for col in columnNames}
        data.rename(columns=newNames, inplace=True)
        msg = ''
        failed = False
        print(newNames)
        print(data.dtypes)

        columns_needed = {'style', 'size', 'color', 'company',
                          'warehouse', 'orderdate', 'ordered'}
        columns_available = set(newNames.values())
        missing = columns_needed.difference(columns_available)

        if len(missing) > 0:
            msg = "Import failed. Please make sure these columns are present in import file: 'style', 'size', 'color', 'company', 'warehouse', 'order date', 'ordered'"
            failed = True
            return errors, msg, failed

        try:
            data['orderdate'] = data['orderdate'].apply(convert_date)
            data['orderdate'] = data['orderdate'].astype('datetime64')
        except Exception as err:
            msg = 'Import Failed. Please make sure Order Date column has dates as mm/dd/yyyy or mm/dd or empty values'
            failed = True
            return errors, msg, failed

        for index, row in data.iterrows():
            print(row)

            try:
                purchase = Purchase()
                purchase.status = 'In Transit'
                purchase.style = '' if pd.isna(row['style']) else str(row['style']).strip()
                purchase.size = '' if pd.isna(row['size']) else str(row['size']).strip()
                purchase.color = '' if pd.isna(row['color']) else str(row['color']).strip()
                purchase.company = '' if pd.isna(row['company']) else str(row['company']).strip()
                purchase.warehouse = '' if pd.isna(row['warehouse']) else str(row['warehouse']).strip()
                purchase.ordered = int(row['ordered'])
                purchase.orderDate = row['orderdate'].date()
                days_add = 10 if purchase.warehouse.upper() == 'BE' else 5
                purchase.arrivalDate = purchase.orderDate + timedelta(days=days_add)
                purchase.sfmId = purchase.style + '-' + purchase.size + '-' + purchase.color
                purchase.save()
                Utilities.update_inventory(purchase)
            except Exception as e:
                errors.append('error row ' + str(index+2) + ': ' + str(e))

        if len(errors) > 0:
            msg = 'Some records were not imported'
        else:
            msg = 'Successfully imported all records'

        return errors, msg, failed





