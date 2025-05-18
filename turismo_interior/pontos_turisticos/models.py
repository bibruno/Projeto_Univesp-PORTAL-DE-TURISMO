from django.db import models

# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class TouristSpot(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    address = models.TextField()
    rating = models.FloatField()
    place_id = models.CharField(max_length=100, unique=True)
    types = models.ManyToManyField(Type)

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
