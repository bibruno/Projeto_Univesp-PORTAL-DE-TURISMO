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

class CityType(models.Model):
    city = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('city', 'type')
    
    def __str__(self):
        return f"{self.city} - {self.type}"

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city_type = models.ForeignKey(CityType, on_delete=models.CASCADE, related_name='cities')
        
    def __str__(self):
        return self.name
