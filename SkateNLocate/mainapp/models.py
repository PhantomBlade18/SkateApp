from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
 

"""
    Skateboard assignment guide
    1- Skateboard
    2- Any
    3- Longboard

    any put in the middle as it is equally as close to both in euclidean values hence easier more fitting when user
    has no preference
"""

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length = 75)
    long = models.FloatField()
    lat = models.FloatField()
    avgRating = models.FloatField(default = 0)
    avgSurface = models.FloatField(default = 0)
    avgPopularity = models.FloatField(default = 0)
    ramps = models.IntegerField(default = 0)
    indoor = models.IntegerField(default = 0)
    paid = models.IntegerField(default = 0)
    cruising = models.IntegerField(default = 0)
    asphalt= models.IntegerField(default = 0)
    concrete = models.IntegerField(default = 0)
    wood = models.IntegerField(default = 0)
    skateType = models.IntegerField(default = 2)


    def calcRating(self):
        o = self.ratings.all().aggregate(Avg('overall'),Avg('surface'),Avg('popularity'))
        self.avgRating = o['overall__avg']
        self.avgSurface = o['surface__avg']
        self.avgPopularity = o['popularity__avg']


    def __str__(self):
        x = "Name: "+self.name+ " Lat: "+ str(self.lat)+" Long: "+ str(self.long)+ " Overall Rating: " +str(self.avgRating) + " Surface Rating: " +str(self.avgSurface )+ " Popularity Rating: " +str(self.avgPopularity) + " ramp: " +str(self.ramps)+" indoor: " +str(self.indoor)+" paid: " +str(self.paid)+"cruising: " +str(self.cruising)+" asphalt: " +str(self.asphalt)+" concrete: " +str(self.concrete)+" wood :" +str(self.wood)+ " board: " +str(self.skateType)+ "\n"
        return x
    
    def switch(self):
        a = self.long
        self.long = self.lat
        self.lat = a

class Member(User):

    avgRating = models.FloatField(default = 0)
    avgSurface = models.FloatField(default = 0)
    avgPopularity = models.FloatField(default = 0)
    ramps = models.IntegerField(default = 0)
    indoor = models.IntegerField(default = 0)
    paid = models.IntegerField(default = 0)
    cruising = models.IntegerField(default = 0)
    asphalt= models.IntegerField(default = 0)
    concrete = models.IntegerField(default = 0)
    wood = models.IntegerField(default = 0)
    skateType = models.IntegerField(default = 2)

    def calcRating(self):
        o = self.userRatings.all().aggregate(Avg('overall'),Avg('surface'),Avg('popularity'))
        self.avgRating = o['overall__avg']
        self.avgSurface = o['surface__avg']
        self.avgPopularity = o['popularity__avg']

    def __str__(self):
        x = "Name: "+self.get_username()+ " Overall Rating: " +str(self.avgRating) + " Surface Rating: " +str(self.avgSurface) + " Popularity Rating: " +str(self.avgPopularity) +  " ramp: " +str(self.ramps)+" indoor: " +str(self.indoor)+" paid: " +str(self.paid)+"cruising: " +str(self.cruising)+" asphalt: " +str(self.asphalt)+" concrete: " +str(self.concrete)+" wood :" +str(self.wood)+ " board: " +str(self.skateType)+"\n"
        return x

class Rating(models.Model):
    location = models.ForeignKey(to= Location,related_name= "ratings",null= True,on_delete= models.CASCADE)
    author = models.ForeignKey(to= Member,related_name= "userRatings",null = True, on_delete = models.CASCADE)
    overall = models.IntegerField(default = 0)
    surface = models.IntegerField(default = 0)
    popularity = models.IntegerField(default = 0)

    def __str__(self):
        return "Skatepark: "+ self.location.name+ " User: "+ self.author.get_username()+ " Overall Rating: " +str(self.overall) + " Surface Rating: " +str(self.surface) + " Popularity Rating: " +str(self.popularity) +  "\n"