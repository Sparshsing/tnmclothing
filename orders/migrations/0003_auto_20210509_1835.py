# Generated by Django 3.2 on 2021-05-09 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_sfmid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='buyerComments',
            field=models.CharField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='order',
            name='buyerEmail',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='buyerName',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='customerPaidShipping',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='order',
            name='design',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='giftMessages',
            field=models.CharField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='order',
            name='orderStatus',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='printed',
            field=models.CharField(blank=True, max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='priorityShip',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='productAvailability',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='saleDate',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='sfmNotes',
            field=models.CharField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='sku',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='trackingNumber',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]