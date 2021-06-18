# Generated by Django 3.2 on 2021-06-02 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('storeName', models.CharField(max_length=50)),
                ('invoiceNo', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(max_length=10)),
                ('notes', models.CharField(max_length=500)),
                ('subTotal', models.DecimalField(decimal_places=2, max_digits=5)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('taxrate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipDate', models.DateField()),
                ('orderDate', models.DateField()),
                ('orderNo', models.CharField(max_length=20)),
                ('customer', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoiceItem', to='invoices.invoice')),
            ],
        ),
    ]