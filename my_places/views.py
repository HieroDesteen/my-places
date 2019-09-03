from django.shortcuts import render, redirect
import my_places.utils as r
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# @login_required(login_url='/login')
def index(request):
    # location = '48.5609974,35.142040099999996'
    # radius = 50000
    # my_places = r.MyPlaces(location, radius)
    # for place in my_places:
    #     pass
    if request.user.is_authenticated:
        return HttpResponse("Залогинен")
    else:
        return HttpResponse("Не залогинен")


def login_view(request):
    if 'username' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main page')
        else:
            return HttpResponse("Check password or smth...")

    return render(request, "login.html")
