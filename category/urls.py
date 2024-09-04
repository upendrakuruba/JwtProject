from django.urls import path
from .views import *
urlpatterns = [
    path("", Productlc.as_view(), name="getproduct"),
    path("<int:_id>/", Productrud.as_view(), name="Productrud"),
]
