# Generated by Django 3.2 on 2021-06-18 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0005_remove_invoice_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='attachment',
            field=models.FileField(null=True, upload_to='invoicepdfs/'),
        ),
    ]
