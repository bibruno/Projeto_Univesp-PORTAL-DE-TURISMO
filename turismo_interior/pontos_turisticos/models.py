from django.db import models

# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class TouristSpot(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100, db_index=True)
    rating = models.FloatField()
    types = models.ManyToManyField(Type)
    latitude = models.FloatField()
    longitude = models.FloatField()
    place_id = models.CharField(max_length=100, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['city', 'rating']),
        ]

    def __str__(self):
        return self.name
