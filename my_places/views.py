from django.shortcuts import render, redirect
import my_places.utils as r
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from my_places.forms import CustomUserCreationForm
from my_places.models import CurrentResidence, Places

@login_required(login_url='logging page')
def index(request):
    if request.method == 'POST':
        location = str(request.POST.get('lat')) + ',' + str(request.POST.get('lng'))
        res = CurrentResidence.create_residence(location, request.user.username)
        if 'radius' in request.POST and request.POST['radius'] != '':
            radius = request.POST.get('radius')
            my_places = r.ApiResponse(location, radius)
        else:
            my_places = r.ApiResponse(location)
        for places in my_places:
            for place in places:
                r.SavingIntoDB.save_place(place, res)

        my_places.main_upload()
        return redirect('places page')
        # for placess in my_places:
        #     data = {'places': placess}
        #     response = places(request, data)
        # return render(request, "index.html", context=data)

    return render(request, "index.html")


@login_required(login_url='logging page')
def places(request):
    context = {'residences': CurrentResidence.residences_by_user(request.user.username)}
    if request.method == 'POST':
        residence = request.POST.get('residence')
        context['places'] = Places.places_by_residence(residence)

    return render(request, "places.html", context=context)


def logout_request(request):
    logout(request)
    return redirect('logging page')


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


def user_register(request):
    data = {'form': CustomUserCreationForm()}
    if request.method == 'POST':
        new_user = CustomUserCreationForm(request.POST)
        print(new_user)
        if new_user.is_valid():
            new_user.save()
            user = authenticate(request, username=new_user.cleaned_data['username'],
                                password=new_user.cleaned_data['password2'])
            login(request, user)
            return redirect('main page')
        else:
            data['errors'] = new_user.errors

    return render(request, 'register.html', context=data)
