# Generated by Django 3.2 on 2021-05-12 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_order_productavailability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customerPaidShipping',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]