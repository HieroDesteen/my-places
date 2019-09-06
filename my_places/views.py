from django.shortcuts import render, redirect
import my_places.utils as r
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from my_places.forms import CustomUserCreationForm


@login_required(login_url='logging page')
def index(request):
    if request.method == 'POST':
        location = str(request.POST.get('lat')) + ',' + str(request.POST.get('lng'))
        res = r.CurResidence(location, request.user.username).create_location()
        if 'radius' in request.POST:
            radius = request.POST.get('radius')
            my_places = r.MyPlaces(location, res, radius)
        else:
            my_places = r.MyPlaces(location, res)
        my_places.main_upload()
        return redirect('places page')
        # for placess in my_places:
        #     data = {'places': placess}
        #     response = places(request, data)
        # return render(request, "index.html", context=data)

    return render(request, "index.html")


@login_required(login_url='logging page')
def places(request):
    ret = r.ReturnPlaces(request.user.username)
    context = {'residences': ret.return_residences()}
    if request.method == 'POST':
        residence = request.POST.get('residence')
        context['places'] = ret.places_by_res(residence)

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
            user = authenticate(request, username=new_user.cleaned_data['username'], password=new_user.cleaned_data['password2'])
            login(request, user)
            return redirect('main page')
        else:
            data['errors'] = new_user.errors['password2']

    return render(request, 'register.html', context=data)
