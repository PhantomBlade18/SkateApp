from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse ,Http404, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
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
    if 'username' and 'password' and 'email' in request.POST:
        u = request.POST['username']
        p = request.POST['password']
        e = request.POST['email']
        ramps= int(request.POST['ramps'])
        indoor=int(request.POST['indoor'])
        paid=int(request.POST['paid'])
        cruising=int(request.POST['cruising'])
        asphalt=int(request.POST['asphalt'])
        concrete=int(request.POST['concrete'])
        wood=int(request.POST['wood'])
        skateType=int(request.POST['board'])
        user = Member(username = u, email = e, ramps = ramps,indoor = indoor,paid = paid,cruising = cruising,asphalt = asphalt,concrete = concrete ,wood = wood,skateType = skateType)
        user.set_password(p)
        try: user.save()
        except IntegrityError: raise Http404('Username ' +u+' already taken: Usernames must be unique')
        request.session['username'] = u
        request.session['password'] = p
        request.session['loggedin'] = True
        context = {'user': u ,'loggedin': True}
        return HttpResponseRedirect(reverse('index'))

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

@loggedin
def updateEmail(request, user):
    if request.method == "POST":
        email = request.POST['email']
        user.email = email
        user.save()
        context = {'successful': True,'msg': "Email updated successfully"}
        return JsonResponse(context, safe = False)
    else:
        raise Http404("Something went wrong.")

@loggedin
def updatePassword(request, user):
    if request.method == "POST":
        cpassword = request.POST['currentPassword']
        npassword = request.POST['newPassword']
        if user.check_password(cpassword):
            user.set_password(npassword)
            user.save()
            context = {'successful': True , 'msg': "Password Updated Successfully!"}
            return JsonResponse(context)
        else:
            context = {'successful': False , 'msg': "The current password is incorrect!"}
            return JsonResponse(context)
    else:
        raise Http404("Something went wrong.")

@loggedin
def updatePrefs(request,user):
    if request.method == "POST":
            user.ramps= int(request.POST['ramps'])
            user.indoor=int(request.POST['indoor'])
            user.paid=int(request.POST['paid'])
            user.cruising=int(request.POST['cruising'])
            user.asphalt=int(request.POST['asphalt'])
            user.concrete=int(request.POST['concrete'])
            user.wood=int(request.POST['wood'])
            user.skateType=int(request.POST['board'])
            user.save()
            context = {'successful': True , 'msg': "Preferences Updated Successfully!"}
            return JsonResponse(context)
        
    else:
        raise Http404("Invalid Request Type.")

# Create your views here.
def index(request):
    if 'username' in request.session:
        user = Member.objects.get(username = request.session['username'])
        context = {'user': user ,'loggedin': True}
        spare() #quick test
        return render(request,'mainapp/home.html',context)
    else:
        spare()
        return render(request,'mainapp/home.html')
@loggedin
def myRecommendations(request,user):
    if 'username' in request.session:
        context = {'user': user ,'loggedin': True}
        spare() #quick test
        return render(request,'mainapp/recommendations.html',context)
    else:
        spare()
        return render(request,'mainapp/login.html')

@loggedin
def viewProfile(request, user):
    username = request.session['username']
    context = {'user': user, 'loggedin': True}
    return render(request, 'mainapp/profile.html', context)


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


@loggedin
def getRecommendations(request,user):
    locs = Location.objects.all() 
    df = read_frame(locs)
    me = MemberSerializer(user).data
    #print(get_skate_recommendations(df,me).to_string())
    locs = Location.objects.all() 
    df = read_frame(locs)
    print("This is  the latitude :", request.POST['lat'])
    loc = (request.POST['lat'],request.POST['lng'])
    df['distance'] = df.apply(lambda row:distance.distance(loc,(row.lat,row.long)).km,axis = 1)
    #df = df[df['distance']<= 20]
    if 'username' in request.session:
        context = { 'loggedin':True,'skateparks':df.to_json(orient = "records")}
    else:
        context = { 'loggedin':False,'skateparks':df.to_json(orient = "records")}

    return JsonResponse(context, safe = False)
    print(df.to_string())

def spare(): #Code for algo
    locs = Location.objects.all() 
    df = read_frame(locs)
    
    #print(df.to_string())
    
    mem = Member.objects.get(pk=1)
    print(mem)
    me = MemberSerializer(mem).data

    print(get_skate_recommendations(df,me).to_string())
    
    locs = Location.objects.all() 
    df = read_frame(locs)
    loc = (51.548600,-0.367310)
    df['distance'] = df.apply(lambda row:distance.distance(loc,(row.lat,row.long)).km,axis = 1)

    print(df.to_string())
    #return HttpResponse("Hello World")

    #Boop