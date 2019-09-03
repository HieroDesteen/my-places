from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="main page"),
    path('login', views.login_view, name="logging page")
]
