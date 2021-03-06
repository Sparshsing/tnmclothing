# Generated by Django 3.2 on 2021-05-17 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sfmId', models.CharField(max_length=50, unique=True)),
                ('style', models.CharField(max_length=30)),
                ('size', models.CharField(max_length=5)),
                ('color', models.CharField(max_length=25)),
                ('inStock', models.IntegerField()),
                ('arrivalDate', models.DateField()),
                ('minimum', models.IntegerField()),
                ('maximum', models.IntegerField()),
            ],
        ),
    ]
