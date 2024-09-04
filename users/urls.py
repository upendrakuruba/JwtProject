from django.urls import path
from .views import MyTokenObtainPairView
from  users.views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("register/", registeruser.as_view(), name="register"),
    path("login/", MyTokenObtainPairView.as_view(),name='login'),
    path('profile/', getUserProfile, name='profile'),
    path('getusers/', getUsers, name='getusers'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("activate/<uidb64>/<token>/",activate, name="activate"),
    path('PasswordResetEmail/', PasswordResetEmail.as_view(), name='PasswordResetEmail'),
    path('PasswordTokenCheckAPI/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='PasswordTokenCheckAPI'),
    path('SetNewpassword/', SetNewpassword.as_view(), name='SetNewpassword'),

    # path("login/", LoginView.as_view(), name="LoginView"),
    # path("userview/", UserView.as_view(), name="userview"),
    # path("logout/", LogoutView.as_view(), name="LogoutView"),
]
