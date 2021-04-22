from django.test import TestCase,Client
from django.urls import reverse
from mainapp.models import Location,Member,Rating
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.a_url = reverse('index')

    def test_index(self):
        response = self.client.get(self.a_url)

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'mainapp/home.html')

    def test_new_user(self):
        response = self.client.post(reverse('registerUserView'),{
            'username': 'LarryTheSkater',
            'password': 'LegendaryLarry105',
            'email':'RobertDestroyer@boop.com',
            'ramps': '1',
            'indoor': '1',
            'paid':'1', 
            'cruising':'0',
            'asphalt':'0',
            'concrete': '1',
            'wood': '1',
            'board':'1'})

        self.assertEquals(response.status_code,302)
        self.assertEquals(Member.objects.count(),1)
        #self.assertEquals()


        
               
