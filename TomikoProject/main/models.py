from django.db import models


class Brands(models.Model):
    country = models.CharField(max_length=50)
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
    brand_country = models.ForeignKey('Brands', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cars'


class Reviews(models.Model):
    user_name = models.CharField(max_length=255)
    rating = models.FloatField()
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'reviews'


class Feedback(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    message = models.CharField(max_length=200)

    class Meta:
        db_table = 'feedback'


class Clips(models.Model):
    cover_url = models.CharField(max_length=200)
    link = models.CharField(max_length=200)

    def __str__(self):
        return f"Clip {self.id}: {self.cover_url}"
    
    class Meta:
        managed = False  
        db_table = 'clips'