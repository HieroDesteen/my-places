import urllib.request
import urllib.parse
import json

key = 'AIzaSyDbkfSHOrrs59qQj4I1WVb0ORj3Wll8oqI'
url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'


def url_creation(token=None):
    if token is None:
        r_params = {
            'radius': '50000',
            'key': key,
            'location': '48.5609974,35.142040099999996',
        }
    else:
        r_params = {
            'key': key,
            'pagetoken': r['next_page_token']
        }
    data = urllib.parse.urlencode(r_params)
    req = url + '?' + data
    return req


def response(full_url):
    with urllib.request.urlopen(full_url) as f:
        resp = json.load(f)
    return resp
