from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse ,Http404
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
            return render(request, 'mainapp/home.html', context)
        else:
            raise Http404("Username or Password is Incorrect")

@loggedin
def logout(request, user):
    request.session.flush()
    return render(request,'mainapp/home.html')

# Create your views here.
def index(request):
    return render(request,'mainapp/home.html')

def viewProfile(request):
    return render(request,'mainapp/home.html')

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
            df['distance'] = df.apply(lambda row:distance.distance(loc,(row.lat,row.long)).km,axis = 1)
            df = df[df['distance']<= 20]
            print(df.to_string())
            context = df.to_json(orient = "records")
            return JsonResponse(context, safe = False)
            print("Return not performed")


        
            
            

def get_skate_recommendations(df: pd.DataFrame, user_features: dict) -> pd.DataFrame: #ensures a pandas dataframe is returned. we pass the original df and the target anchor(who we compare against)
    features = ['avgRating','avgSurface','avgPopularity'] #list of features that are used to compute similarity between the users average ratings  and the skate parks average
    

    #create the features in a seperate frame
    df_features = df[features].copy()
    #df_features = normalize_features(df_features)

    df_user = pd.DataFrame([user_features])
    df_features = pd.concat([df_user, df_features], sort=False)
    df_features = normalize_features(df_features)
    
    # compute the distances
    X = df_features.values
    Y = df_features.values[0].reshape(1, -1)
    distances = euclidean_distances(X, Y)
    
    df_sorted = df.copy()
    
    df_sorted['similarity_distance'] = distances[1:]
    return df_sorted.sort_values('similarity_distance').reset_index(drop=True)


def normalize_features(df):
    for col in df.columns:
        # fill any NaN's with the mean
        df[col] = df[col].fillna(df[col].mean())
        df[col] = StandardScaler().fit_transform(df[col].values.reshape(-1, 1))
    return df

def signup(request):
    return render(request,'mainapp/register.html')


def spare(): #Code for algo
    locs = Location.objects.all() 
    df = read_frame(locs)
    
    #print(df.to_string())
    
    mem = Member.objects.get(pk=1)

    me = MemberSerializer(mem).data

    #print(get_skate_recommendations(df,me).to_string())
    
    locs = Location.objects.all() 
    df = read_frame(locs)
    loc = (51.548600,-0.367310)
    df['distance'] = df.apply(lambda row:distance.distance(loc,(row.lat,row.long)).km,axis = 1)
    print(df.to_string())
    #return HttpResponse("Hello World")