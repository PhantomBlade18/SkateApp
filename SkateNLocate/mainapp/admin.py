from django.contrib import admin
from mainapp.models import Location,Member,Rating

# Register your models here.
admin.site.register(Location)
admin.site.register(Member)
admin.site.register(Rating)