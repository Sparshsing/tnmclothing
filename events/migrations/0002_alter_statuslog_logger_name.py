# Generated by Django 3.2 on 2021-06-05 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuslog',
            name='logger_name',
            field=models.CharField(max_length=300),
        ),
    ]
