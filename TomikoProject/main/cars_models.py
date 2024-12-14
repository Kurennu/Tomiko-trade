from django.db import models


class Brands(models.Model):
    country = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'brands'


class Cars(models.Model):
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    mileage = models.IntegerField()
    price = models.IntegerField()
    transmission = models.CharField(max_length=50)
    engine_volume = models.CharField(max_length=50)
    drive = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    power_volume = models.CharField(max_length=50)
    brand_country = models.ForeignKey(Brands, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cars'
