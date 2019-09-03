from django.shortcuts import render
import my_places.utils as r

def index(request):
    location = '48.5609974,35.142040099999996'
    radius = 50000
    my_places = r.MyPlaces(location, radius)
    for place in my_places:
        pass

    return render(request, "main_page/index.html")
