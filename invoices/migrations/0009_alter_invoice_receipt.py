# Generated by Django 3.2 on 2021-07-04 09:11

from django.db import migrations, models
import invoices.models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0008_alter_invoice_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='receipt',
            field=models.FileField(blank=True, null=True, upload_to=invoices.models.receipt_path),
        ),
    ]
