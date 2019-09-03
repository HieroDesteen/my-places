from my_places.models import Places, Types
import urllib.request
import urllib.parse
import json
import places.settings as settings

url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'


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
                'location': self.location,
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
        for res in results:
            p = Places()
            p.name = res['name']
            p.place_id = res['place_id']
            if 'price_level' in res:
                p.price_level = res['price_level']
            if 'rating' in res:
                p.rating = res['rating']
            if 'vicinity' in res:
                p.vicinity = res['vicinity']
            if 'formatted_address' in res:
                p.formatted_address = res['formatted_address']
            if 'permanently_closed' in res:
                p.permanently_closed = res['permanently_closed']
            p.save()
            if 'types' in res:
                for type in res['types']:
                    t, created = Types.objects.get_or_create(type=type)
                    t.save()
                    p.types.add(t)
            places.append((tuple(p, res['types'])))
        if 'next_page_token' in response:
            self.token = response['next_page_token']
            return places, True
        else:
            return places, False
