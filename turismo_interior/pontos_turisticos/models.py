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
    address = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    place_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='pontos_turisticos/', null=True, blank=True)
    types = models.ManyToManyField(Type, blank=True)

    def __str__(self):
        return self.name

class CityType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.ForeignKey(CityType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
