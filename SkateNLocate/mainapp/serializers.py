from mainapp.models import Location,Member,Rating
from rest_framework import serializers



class LocationSerializer(serializers.ModelSerializer):
 class Meta:
  model = Location
  fields = [
   'name',
   'long',
   'lat',
   'avgRating',
   'avgSurface',
   'avgPopularity',
  ]

class MemberSerializer(serializers.ModelSerializer):
 class Meta:
  model = Member
  fields = [
   
   'avgRating',
   'avgSurface',
   'avgPopularity',
  ]

class RatingSerializer(serializers.ModelSerializer):
 class Meta:
  model = Rating
  fields = [
   'location',
   'author',
   'avgRating',
   'avgSurface',
   'avgPopularity',
  ]