from django.urls import path
from .views import *

urlpatterns = [
    path('',UserLogin.as_view()),
    path('login/',UserLogin.as_view(), name="login"),
    path('logout/',UserLogout.as_view(), name="logout"),
    path('sign-up/',UserSignUp.as_view(), name="sign_up"),
    path('dashboard/',Dashboard.as_view(), name="dashboard"),
    path('setup/forgot-pass/',SetUpForgotPassword.as_view(), name="setup_forgot_pass"),
    path('forgot-pass/',ForgotPassword.as_view(), name="forgot_pass"),
]