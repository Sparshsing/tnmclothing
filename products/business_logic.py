from .models import Product
import pandas as pd
from datetime import timedelta

class ImportFiles:
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
                product.style = '' if pd.isna(row['style']) else str(row['style'])
                product.size = '' if pd.isna(row['size']) else str(row['size'])
                product.color = '' if pd.isna(row['color']) else str(row['color'])
                product.sku = '' if pd.isna(row['sku']) else str(row['sku'])
                product.cost = None if pd.isna(row['cost']) else float(row['cost'])
                product.price = None if pd.isna(row['price']) else float(row['price'])
                product.sfmId = product.style + '-' + product.size + '-' + product.color
                product.save()
            except Exception as e:
                errors.append('error row ' + str(index+1) + ': ' + str(e))

        return errors


