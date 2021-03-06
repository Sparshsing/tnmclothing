# Generated by Django 3.2 on 2021-05-07 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('storeName', models.CharField(max_length=50, unique=True)),
                ('storeCode', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('emailAddress', models.CharField(max_length=50)),
                ('addressLine1', models.CharField(max_length=50)),
                ('addressLine2', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
                ('zipCode', models.IntegerField(max_length=5)),
            ],
        ),
    ]
