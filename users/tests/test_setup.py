from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker

class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.fake = Faker()
        self.user_data ={
            'first_name':self.fake.email(),
            'last_name':self.fake.email(),
            'email':self.fake.email(),
            'username':self.fake.email(),
            'password':self.fake.email(),
        }
        return super().setUp()


    def tearDown(self):
        return super().tearDown()

    