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
        msg = ''
        failed = False

        columns_needed = {'price', 'sku', 'style', 'size', 'color'}
        columns_available = set(newNames.values())
        missing = columns_needed.difference(columns_available)

        if len(missing) > 0:
            msg = "Import failed. Please make sure these columns are present in import file: 'price', 'sku', 'style', 'size', 'color'"
            failed = True
            return errors, msg, failed

        try:
            data['price'].astype('float64')
        except Exception as err:
            msg = 'Import Failed. Please make sure Price column has numbers only'
            failed = True
            return errors, msg, failed

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
                product.price = None if pd.isna(row['price']) else float(row['price'])
                product.sfmId = product.style + '-' + product.size + '-' + product.color
                product.save()
                # inventory record will be created using signals mechanism
                # Utilities.create_inventory_record(product)
            except Exception as e:
                errors.append('error row ' + str(index+2) + ': ' + str(e))

        if len(errors) > 0:
            msg = 'Some records were not imported'
        else:
            msg = 'Successfully imported all records'
        return errors, msg, failed




