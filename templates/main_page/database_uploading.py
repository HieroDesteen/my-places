from my_places.models import Places, Types
from django.shortcuts import get_object_or_404
from django.http import Http404


def main_upload(response):
    results = response['results']
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
                try:
                    t = get_object_or_404(Types, type=type)
                    p.types.add(t)
                except Http404:
                    t = Types()
                    t.type = type
                    t.save()
                    p.types.add(t)