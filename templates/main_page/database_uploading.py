from my_places.models import Places, Types


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
                t, created = Types.objects.get_or_create(type=type)
                t.save()
                p.types.add(t)
