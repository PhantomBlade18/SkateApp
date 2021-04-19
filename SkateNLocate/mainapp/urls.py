from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Nearby/',views.getNearestSkateparks,name='getSkateParks'),
    path('MyRecommendations/', views.myRecommendations, name='MyRecommendations'),
    path('MyRecommendations/Recommendations/',views.getRecommendations,name='Recommendations'),
    path('register/', views.signup, name='signup'),
    path('registerUser/', views.registerUserView, name = 'registerUserView'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('Profile/', views.viewProfile, name='viewProfile'),
    path('Profile/updateEmail/', views.updateEmail, name='updateEmail'),
    path('Profile/updatePassword/', views.updatePassword, name='updatePassword'),
    path('Profile/updatePreferences/', views.updatePrefs, name='updatePrefs'),
    path('submitRating/', views.submitRating, name='submitRating'),
    ]