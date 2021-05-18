from .models import Product
import pandas as pd
from inventory.models import Inventory
from datetime import timedelta, date, datetime

class Utilities:

    @staticmethod
    def create_inventory_record(p):
        new_inventory = Inventory(sfmId=p.sfmId, style=p.style, size=p.size, color=p.color, inStock=0,
                                  arrivalDate=date.today(), minimum=0, maximum=100)
        new_inventory.save()

    @staticmethod
    def import_products(data):

        errors = []
        columnNames = list(data)
        # renaming columns to avoid problems with Case and spaces
        newNames = {col: col.strip().replace(' ', '').lower() for col in columnNames}
        data.rename(columns=newNames, inplace=True)
        data['cost'].astype('float64')
        data['price'].astype('float64')
        print(newNames)
        print(data.dtypes)
        
        for index, row in data.iterrows():
            print(row)

            try:
                product = Product()
                product.style = '' if pd.isna(row['style']) else str(row['style']).strip()
                product.size = '' if pd.isna(row['size']) else str(row['size']).strip()
                product.color = '' if pd.isna(row['color']) else str(row['color']).strip()
                product.sku = '' if pd.isna(row['sku']) else str(row['sku']).strip()
                product.cost = None if pd.isna(row['cost']) else float(row['cost'])
                product.price = None if pd.isna(row['price']) else float(row['price'])
                product.sfmId = product.style + '-' + product.size + '-' + product.color
                product.save()
                Utilities.create_inventory_record(product)
            except Exception as e:
                errors.append('error row ' + str(index+1) + ': ' + str(e))

        return errors




