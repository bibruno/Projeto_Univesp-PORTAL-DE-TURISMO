from django.db import models

# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class TouristSpot(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    rating = models.FloatField(null=True, blank=True)
    place_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    types = models.ManyToManyField(Type, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['city']),
        ]

class CityTypes(models.Model):
    city = models.CharField(max_length=100, db_index=True)
    type_name = models.CharField(max_length=100)
    count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('city', 'type_name')
        verbose_name = 'City Type'
        verbose_name_plural = 'City Types'
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['type_name']),
        ]
    
    def __str__(self):
        return f"{self.city} - {self.type_name} ({self.count})"
