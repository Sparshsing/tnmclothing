from .models import Purchase
import pandas as pd
from datetime import timedelta

class ImportFiles:
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
                purchase.status = 'in transit'
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
            except Exception as e:
                errors.append('error row ' + str(index+1) + ': ' + str(e))

        return errors


