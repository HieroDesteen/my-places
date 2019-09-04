from django.shortcuts import render, redirect
import my_places.utils as r
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='logging page')
def index(request):
    if request.method == 'POST':
        location = tuple((request.POST.get('lat', request.POST.get('lng'))))
        if 'radius' in request.POST:
            radius = request.POST.get('radius')
        my_places = r.MyPlaces(location, radius)
        for place in my_places:
            pass

    return render(request, "index.html")


def logout_request(request):
    logout(request)
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main page')
        else:
            return HttpResponse("Check password or smth...")

    return render(request, "login.html")
