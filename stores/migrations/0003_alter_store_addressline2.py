# Generated by Django 3.2 on 2021-05-08 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_auto_20210507_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='addressLine2',
            field=models.CharField(max_length=50),
        ),
    ]
