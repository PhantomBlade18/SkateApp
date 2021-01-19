from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length = 75)
    long = models.FloatField()
    lat = models.FloatField()
    avgRating = models.FloatField(default = 0)
    avgSurface = models.FloatField(default = 0)
    avgPopularity = models.FloatField(default = 0)




class Member(User):

    avgRating = models.FloatField(default = 0)
    avgSurface = models.FloatField(default = 0)
    avgPopularity = models.FloatField(default = 0)

class Rating(models.Model):
    location = models.ForeignKey(to= Location,related_name= "ratings",null= True,on_delete= models.CASCADE)
    author = models.ForeignKey(to= Member,related_name= "userRatings",null = True, on_delete = models.CASCADE)
    overall = models.IntegerField(default = 0)
    surface = models.IntegerField(default = 0)
    popularity = models.IntegerField(default = 0)