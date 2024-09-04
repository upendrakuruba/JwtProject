from django.urls import path
from .views import *
urlpatterns = [
    path("", Incomelc.as_view(), name="getIncome"),
    path("<int:id>/", Incomerud.as_view(), name="Incomerud"),
]
