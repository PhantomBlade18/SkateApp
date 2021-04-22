from django.test import SimpleTestCase
from django.urls import reverse,resolve
import mainapp.views

class TestURLs(SimpleTestCase):

    def test_list_url_is_resolved(self):
        print("HelloWorld")
