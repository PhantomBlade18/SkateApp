from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recommendations/',views.getNearestSkateparks,name='getSkateParks'),
    path('myRecommendations/',views.getNearestSkateparks,name='myRecommendations'),
    path('register/', views.signup, name='signup'),
    path('registerUser/', views.registerUserView, name = 'registerUserView'),
    path('login/', views.login, name='login'),
    ]