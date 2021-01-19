from django.shortcuts import render
from django.http import HttpResponse
from mainapp.models import Rating,Location,Member
from django_pandas.io import read_frame

# Create your views here.
def index(request):
    locs = Location.objects.all()
    df = read_frame(locs)
    print(df.to_string())
    return HttpResponse("Hello World")
