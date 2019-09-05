from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="main page"),
    path('login', views.login_view, name="logging page"),
    path('logout', views.logout_request, name='logout page'),
    path('places', views.places, name='places page'),
    path('registration', views.user_register, name='register page')
]
