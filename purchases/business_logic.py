from .models import Purchase
import pandas as pd
from datetime import timedelta, date
from products.models import Product
from inventory.models import Inventory

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
        print(newNames)
        print(data.dtypes)
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

        return errors





