# Generated by Django 5.1.4 on 2025-01-27 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_currencyrate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyrate',
            name='currency',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
