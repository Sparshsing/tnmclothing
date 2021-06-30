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
        msg = ''
        failed = False

        columns_needed = {'maximum', 'minimum', 'instock', 'style', 'size', 'color'}
        columns_available = set(newNames.values())
        missing = columns_needed.difference(columns_available)

        if len(missing) > 0:
            msg = "Import failed. Please make sure these columns are present in import file: 'maximum', 'minimum', 'in stock', 'style', 'size', 'color'"
            failed = True
            return errors, msg, failed

        try:
            data['instock'].astype('int64')
            data['minimum'].astype('int64')
            data['maximum'].astype('int64')
        except Exception as err:
            msg = 'Import Failed. Please make sure in stock, minimum and maximum columns have numbers only or empty values'
            failed = True
            return errors, msg, failed

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

        if len(errors) > 0:
            msg = 'Some records were not imported'
        else:
            msg = 'Successfully imported all records'
        return errors, msg, failed




