from my_places.models import Places, Types
import urllib.request
import urllib.parse
import json
import places.settings as settings

url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'


def save_place(place):
    p = Places()
    p.name = place['name']
    p.place_id = place['place_id']
    if 'price_level' in place:
        p.price_level = place['price_level']
    if 'rating' in place:
        p.rating = place['rating']
    if 'vicinity' in place:
        p.vicinity = place['vicinity']
    if 'formatted_address' in place:
        p.formatted_address = place['formatted_address']
    if 'permanently_closed' in place:
        p.permanently_closed = place['permanently_closed']
    p.save()
    if 'types' in place:
        for type in plae['types']:
            t, created = Types.objects.get_or_create(type=type)
            t.save()
            p.types.add(t)


class MyPlaces:
    def __init__(self, location, radius=5000):
        self.radius = radius
        self.location = location
        self.token = None

    def __iter__(self):
        flag = True
        while flag:
            places, flag = self.main_upload()
            yield places

    def url_creation(self):
        if self.token is None:
            r_params = {
                'radius': self.radius,
                'key': settings.GOOGLE_API_KEY,
                'location': (str(self.location[0]) + ', ' + str(self.location[1])),
            }
        else:
            r_params = {
                'key': settings.GOOGLE_API_KEY,
                'pagetoken': self.token
            }
        data = urllib.parse.urlencode(r_params)
        full_url = url + '?' + data
        return full_url

    def create_response(self):
        full_url = self.url_creation()
        with urllib.request.urlopen(full_url) as f:
            resp = json.load(f)
            return resp

    def main_upload(self):
        response = self.create_response()
        results = response['results']
        places = []
        for place in results:
            save_place(place)
            places.append(place)
        if 'next_page_token' in response:
            self.token = response['next_page_token']
            return places, True
        else:
            return places, False
