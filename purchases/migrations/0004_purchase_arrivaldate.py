# Generated by Django 3.2 on 2021-05-10 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0003_remove_purchase_arrivaldate'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='arrivalDate',
            field=models.DateField(null=True),
        ),
    ]