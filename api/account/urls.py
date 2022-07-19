from django.urls import include, path
from django.conf.urls import url

from rest_framework import routers
from . import views


urlpatterns = [
    url(r'signup/$', views.signupView, name="sign_up"),
    url(r'login/$', views.loginView, name="login"),
    url(r'logout/$', views.logOut, name="logout"),
]