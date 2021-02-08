from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length = 75)
    long = models.FloatField()
    lat = models.FloatField()
    avgRating = models.FloatField(default = 0)
    avgSurface = models.FloatField(default = 0)
    avgPopularity = models.FloatField(default = 0)

    def calcRating(self):
        o = self.ratings.all().aggregate(Avg('overall'),Avg('surface'),Avg('popularity'))
        self.avgRating = o['overall__avg']
        self.avgSurface = o['surface__avg']
        self.avgPopularity = o['popularity__avg']


    def __str__(self):
        x = "Name: "+self.name+ "Long: "+ str(self.long)+" Lat: "+ str(self.lat)+ " Overall Rating: " +str(self.avgRating) + " Surface Rating: " +str(self.avgSurface )+ " Popularity Rating: " +str(self.avgPopularity) +  "\n"
        return x  

class Member(User):

    avgRating = models.FloatField(default = 0)
    avgSurface = models.FloatField(default = 0)
    avgPopularity = models.FloatField(default = 0)

    def calcRating(self):
        o = self.userRatings.all().aggregate(Avg('overall'),Avg('surface'),Avg('popularity'))
        self.avgRating = o['overall__avg']
        self.avgSurface = o['surface__avg']
        self.avgPopularity = o['popularity__avg']

    def __str__(self):
        x = "Name: "+self.get_username()+ " Overall Rating: " +str(self.avgRating) + " Surface Rating: " +str(self.avgSurface) + " Popularity Rating: " +str(self.avgPopularity) +  "\n"
        return x

class Rating(models.Model):
    location = models.ForeignKey(to= Location,related_name= "ratings",null= True,on_delete= models.CASCADE)
    author = models.ForeignKey(to= Member,related_name= "userRatings",null = True, on_delete = models.CASCADE)
    overall = models.IntegerField(default = 0)
    surface = models.IntegerField(default = 0)
    popularity = models.IntegerField(default = 0)

    def __str__(self):
        return "Skatepark: "+ self.location.name+ " User: "+ self.author.get_username()+ " Overall Rating: " +str(self.overall) + " Surface Rating: " +str(self.surface) + " Popularity Rating: " +str(self.popularity) +  "\n"