from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse ,Http404, HttpResponseRedirect
from django.urls import reverse
from mainapp.models import Rating,Location,Member
from mainapp.serializers import MemberSerializer
from sklearn.metrics import euclidean_distances
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import json
from geopy import distance


#Imports related to pandas and the recommendation algorithm beyond this point
from django_pandas.io import read_frame
import pandas as pd
import numpy as np
from sklearn.metrics import euclidean_distances
from mainapp.Recommender import get_skate_recommendations

def loggedin(view):
    ''' Decorator that tests whether user is logged in '''
    def mod_view(request):
        if 'username' in request.session:
            username = request.session['username']
            try: user = Member.objects.get(username=username)
            except Member.DoesNotExist: raise Http404('Member does not exist')
            return view(request, user)
        else:
            return render(request,'mainapp/login.html')
    return mod_view

def signup(request):
    return render(request,'mainapp/register.html')

def registerUserView(request): 
    ''' adds new user to the database '''
    if 'username' and 'password' and 'email' and 'dob' in request.POST:
        u = request.POST['username']
        p = request.POST['password']
        e = request.POST['email']
        d = request.POST['dob']
        user = Member(username = u, email = e, DOB = d)
        user.set_password(p)
        try: user.save()
        except IntegrityError: raise Http404('Username ' +u+' already taken: Usernames must be unique')
        context = {
            'username' : u,
            'loggedin': True
        }
        return render(request,'mainapp/home.html',context)

    else:
        raise Http404('POST data missing')

def login(request):
    if  request.method == 'GET':
        return render(request,'mainapp/login.html')
    elif not ('username' in request.POST and 'password' in request.POST) and request.method == 'POST':
        context = {
            'msg': "Please enter the username and password"
            }
        data = json.dumps(context)
        return JsonResponse(data)
    else:
        username = request.POST['username']
        password = request.POST['password']
        try: member = Member.objects.get(username=username)
        except Member.DoesNotExist: raise Http404('User does not exist')
        if member.check_password(password):
            # remember user in session variable
            request.session['username'] = username
            request.session['password'] = password
            request.session['loggedin'] = True
            context = {'user': member ,'loggedin': True}
            return HttpResponseRedirect(reverse('index'))
        else:
            raise Http404("Username or Password is Incorrect")

@loggedin
def logout(request, user):
    request.session.flush()
    return HttpResponseRedirect(reverse('index'))

# Create your views here.
def index(request):
    if 'username' in request.session:
        user = Member.objects.get(username = request.session['username'])
        context = {'user': user ,'loggedin': True}
        return render(request,'mainapp/home.html',context)
    else:
        return render(request,'mainapp/home.html')

@loggedin
def viewProfile(request, user):
    username = request.session['username']
    context = {'user': user, 'loggedin': True}
    return render(request, 'mainapp/profile.html', context)

    #Basic test to see whether Pandas Works with Django (SPOILER: IT DOES)
    """   locs = Location.objects.all() 
    df = read_frame(locs)
    df['distance'] = distance.distance(loc,(df['long'],df['lat']))
    print(df.to_string())
    return HttpResponse("Hello World") """

def getNearestSkateparks(request):
    if request.method == 'POST':
        print("Howdy")
        if 'lat' and 'lng' in request.POST:
            print(request.POST['lat'])
            context = {'example' : "Hello World"}
            context = json.dumps(context)
            
            loc = (request.POST['lat'],request.POST['lng'])
            locs = Location.objects.all()
            df = read_frame(locs)
            df['distance'] = df.apply(lambda row:distance.distance(loc,(row.lat,row.long),ellipsoid='WGS-84').km,axis = 1)
            df = df[df['distance']<= 20]
            print(df.to_string())
            if 'username' in request.session:
                context = { 'loggedin':True,'skateparks':df.to_json(orient = "records")}
            else:
                context = { 'loggedin':False,'skateparks':df.to_json(orient = "records")}
            return JsonResponse(context, safe = False)
            print("Return not performed")

@loggedin
def submitRating(request,user):
    if request.method == 'POST':
        if 'id' and 'avg' and 'sur' and 'pop' in request.POST:
            loc = Location.objects.get(pk=request.POST['id'])
            a = request.POST['avg']
            s = request.POST['sur']
            p = request.POST['pop']
            try: rating = Rating.objects.get(author = user, location = loc)
            except Rating.DoesNotExist:
                rating = Rating(author = user, location= loc, overall =a,surface=s,popularity=p)
                rating.save()
                loc.calcRating()
                user.calcRating()
                user.save()
                loc.save()
                context = {'successful': True , 'msg': "Thank you for rating "+loc.name+"!"}
                return JsonResponse(context,safe = False)
            else:
                a = request.POST['avg']
                s = request.POST['sur']
                p = request.POST['pop']
                rating.overall = a
                rating.surface = s
                rating.popularity = p
                rating.save()
                loc.calcRating()
                user.calcRating()
                loc.save()
                user.save()
                
                context = {'successful': True , 'msg': "Rating for "+loc.name+" has been updated. Thank you!"}
                return JsonResponse(context,safe = False)
        else:
            print("Missing something in post")
    else:
        print("Wrong Method: ",request.method)



def getRecommendations(request):
    #To Be Implemented
    print("Hello")

def spare(): #Code for algo
    locs = Location.objects.all() 
    df = read_frame(locs)
    
    #print(df.to_string())
    
    mem = Member.objects.get(pk=1)

    me = MemberSerializer(mem).data

    print(get_skate_recommendations(df,me).to_string())
    
    locs = Location.objects.all() 
    df = read_frame(locs)
    loc = (51.548600,-0.367310)
    df['distance'] = df.apply(lambda row:distance.distance(loc,(row.lat,row.long)).km,axis = 1)
    print(df.to_string())
    #return HttpResponse("Hello World")