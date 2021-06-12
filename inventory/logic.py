import pandas as pd
from .models import Inventory


class Utilities:

    @staticmethod
    def import_inventory(data):

        errors = []
        columnNames = list(data)
        # renaming columns to avoid problems with Case and spaces
        newNames = {col: col.strip().replace(' ', '').lower() for col in columnNames}
        data.rename(columns=newNames, inplace=True)
        data['instock'].astype('int64')
        data['minimum'].astype('int64')
        data['maximum'].astype('int64')
        print(newNames)
        print(data.dtypes)

        for index, row in data.iterrows():
            print(row)

            try:
                style = '' if pd.isna(row['style']) else str(row['style']).strip()
                size = '' if pd.isna(row['size']) else str(row['size']).strip()
                color = '' if pd.isna(row['color']) else str(row['color']).strip()
                sfm_id = style + '-' + size + '-' + color
                inventory = Inventory.objects.get(sfmId=sfm_id)
                inventory.inStock = None if pd.isna(row['instock']) else int(row['instock'])
                inventory.minimum = None if pd.isna(row['minimum']) else int(row['minimum'])
                inventory.maximum = None if pd.isna(row['maximum']) else int(row['maximum'])
                inventory.save()
            except Exception as e:
                errors.append('error row ' + str(index + 2) + ': ' + str(e))

        return errors




