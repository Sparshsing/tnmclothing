from .models import Purchase
import pandas as pd
from datetime import timedelta, date
from products.models import Product
from inventory.models import Inventory

class Utilities:
    @staticmethod
    def update_inventory(purchase, oldStatus=''):

        product = Product.objects.filter(sfmId=purchase.sfmId).first()
        if product is None:
            Utilities.create_product_inventory(purchase)

        # if creating for first time with status transit
        if oldStatus=='' and purchase.status == 'In Transit':
            return
        if oldStatus != purchase.status:
            inventory = Inventory.objects.filter(sfmId=purchase.sfmId).first()
            if inventory:
                if purchase.status == 'In Transit':
                    inventory.inStock = inventory.inStock - purchase.ordered
                else:
                    inventory.inStock = inventory.inStock + purchase.ordered
                inventory.save()
            else:
                raise Exception('Inventory does not exist')

    @staticmethod
    def create_product_inventory(purchase):
        new_Product = Product(sfmId=purchase.sfmId, style=purchase.style, size=purchase.size, color=purchase.color, cost=0.0, price=0.0)
        new_Product.save()
        in_stock = 0 if purchase.status == 'In Transit' else purchase.ordered
        new_inventory = Inventory(sfmId=purchase.sfmId, style=purchase.style, size=purchase.size, color=purchase.color, inStock=in_stock,
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
                errors.append('error row ' + str(index+1) + ': ' + str(e))

        return errors





