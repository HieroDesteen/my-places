from my_places.models import Places, Types, CurrentResidence, CustomUser
import urllib.request
import urllib.parse
import json
import places.settings as settings

url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'


def save_place(place, c):
    p, created = Places.objects.get_or_create(name=place['name'], place_id=place['place_id'])
    if not created:
        # p.name = place['name']
        # p.place_id = place['place_id']
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
            for type in place['types']:
                t, created = Types.objects.get_or_create(type=type)
                if not created:
                    t.save()
                p.types.add(t)
    c.places.add(p)


class MyPlaces:
    def __init__(self, location, cur_residence, radius=5000):
        self.radius = radius
        self.location = location
        self.token = None
        self.cur_residence = cur_residence

    # def __iter__(self):
    #     flag = True
    #     while flag:
    #         places, flag = self.main_upload()
    #         yield places

    def url_creation(self):
        if self.token is None:
            r_params = {
                'radius': self.radius,
                'key': settings.GOOGLE_API_KEY,
                # 'location': '48.5610067, 35.1420604'
                'location': self.location
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
        # places = []
        for place in results:
            save_place(place, self.cur_residence)
            # places.append(place)
        if 'next_page_token' in response:
            self.token = response['next_page_token']
            self.main_upload()
        #     self.token = response['next_page_token']
        #     return places, True
        # else:
        #     return places, False


class CurResidence:
    def __init__(self, location, username):
        self.location = location
        self.user = CustomUser.objects.get(username=username)

    def create_location(self):
        c = CurrentResidence(current_residence=self.location, user=self.user)
        c.save()
        return c


class ReturnPlaces:
    def __init__(self, username):
        self.username = username

    def return_residences(self):
        a = []
        for e in CurrentResidence.objects.filter(user__username=self.username):  # Вернет QuerySet всех мест текущего пользователя
            a.append(e.current_residence)
        # a = CurrentResidence.objects.all()
        # print(a)
        return a
    def places_by_res(self, res):
        a = []
        for e in Places.objects.filter(currentresidence__current_residence=res):
            a.append(e.name)
        return a
