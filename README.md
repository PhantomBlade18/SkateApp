# SkateApp
University project for 3rd Year
 

How to install Django:
https://docs.djangoproject.com/en/3.2/topics/install/#installing-official-release

Google Maps API:
An API key is needed in order to use the map functionalities of the app.
To access all of the functions, it is recommended to use both the Geocoding API
and the Maps JavaScript API when creating a project on the google cloud platform

How to Run the project:
For this project, conda was used to create a virtual environment in python 3.7

1. Create virtual environment 
$Conda Create --name SkateApp 

2. activate environment
$ conda activate SkateApp

3.Test environment (update your pip too)
$python --version
$pip install --upgrade pip

4.django installation
$pip install django

5. Navigate to project directory which contains manage.py and enter:
$ python manage.py runserver