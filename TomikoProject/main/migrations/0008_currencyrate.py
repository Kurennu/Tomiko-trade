# Generated by Django 5.1.4 on 2025-01-27 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_feedback_clip'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=10)),
                ('rate', models.DecimalField(decimal_places=4, max_digits=10)),
            ],
        ),
    ]
