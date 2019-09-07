from my_places.models import Places, Types, CurrentResidence, CustomUser
import urllib.request
import urllib.parse
import json
import time
import places.settings as settings

url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'


class SavingIntoDB:
    def save_place(self, place, c):
        possible_fields = ['price_level', 'rating', 'vicinity', 'name', 'formatted_address', 'permanently_closed', ]
        values = {field: place[field] for field in possible_fields if field in place}
        p, created = Places.objects.get_or_create(place_id=place['place_id'], defaults=values)
        if not created:
            if 'types' in place:
                for type in place['types']:
                    t, created = Types.objects.get_or_create(type=type)
                    if not created:
                        t.save()
                    p.types.add(t)
        else:
            for key, value in values.items():
                if value != getattr(p, key):
                    setattr(p, key, value)
            p.save()

        c.places.add(p)


# class ApiResponse:
#     def __init__(self, location, radius=5000):
#         self.radius = radius
#         self.location = location
#         self.token = None
#
#     def __iter__(self):
#         flag = True
#         while flag:
#             places, flag = self.main_upload()
#             for place in places:
#                 yield place
#
#     def url_creation(self):
#         if self.token is None:
#             r_params = {
#                 'radius': self.radius,
#                 'key': settings.GOOGLE_API_KEY,
#                 # 'location': '48.5610067, 35.1420604'
#                 'location': self.location
#             }
#         else:
#             r_params = {
#                 'key': settings.GOOGLE_API_KEY,
#                 'pagetoken': self.token
#             }
#         data = urllib.parse.urlencode(r_params)
#         full_url = url + '?' + data
#         return full_url
#
#     def create_response(self):
#         full_url = self.url_creation()
#         with urllib.request.urlopen(full_url) as f:
#             resp = json.load(f)
#             return resp
#
#     def main_upload(self):
#         response = self.create_response()
#         if 'next_page_token' in response:
#             # self.main_upload()
#             self.token = response['next_page_token']
#             return response['results'], True
#         else:
#             return response['results'], False


def ApiResponse2(location, radius=5000, token=None):
    if token is None:
        r_params = {
            'radius': radius,
            'key': settings.GOOGLE_API_KEY,
            'location': location
        }
    else:
        r_params = {
            'key': settings.GOOGLE_API_KEY,
            'pagetoken': token
        }
    with urllib.request.urlopen(url + '?' + urllib.parse.urlencode(r_params)) as f:
        resp = json.load(f)
    for result in resp['results']:
        yield result
    if 'next_page_token' in resp:
        time.sleep(3)
        for result in ApiResponse2(location, radius=radius, token=resp['next_page_token']):
            yield result
