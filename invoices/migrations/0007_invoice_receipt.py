# Generated by Django 3.2 on 2021-07-04 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0006_invoice_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='receipt',
            field=models.FileField(null=True, upload_to='invoicereceipts/'),
        ),
    ]