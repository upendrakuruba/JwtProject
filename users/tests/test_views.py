from .test_setup import *
from ..models import User
from rest_framework import status
class TestViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code,400)



    def test_user_cannot_register_correctly(self):
        res = self.client.post(self.register_url,self.user_data,format="json")
        self.assertEqual(res.status_code,201)



    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url,self.user_data,format="json")
        res=self.client.post(self.login_url,self.user_data,format="json")
        self.assertEqual(res.status_code,401)

    def test_user_can_login_after_verified_email(self):
        response=self.client.post(self.register_url,self.user_data,format="json")
        email=response.data['email']
        user= User.objects.get(email=email)
        user.is_active = True
        user.save()
        res=self.client.post(self.login_url,self.user_data,format="json")
        self.assertEqual(res.status_code,status.HTTP_200_OK)