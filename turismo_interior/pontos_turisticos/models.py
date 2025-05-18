class TouristSpot(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    rating = models.FloatField(null=True, blank=True)
    place_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    types = models.ManyToManyField(Type, blank=True)

    def __str__(self):
        return self.name 