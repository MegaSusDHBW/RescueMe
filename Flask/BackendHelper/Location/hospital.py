from googleplaces import GooglePlaces, types, lang
import requests
import json
import os

# Google Places API
API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')

# Initialising the GooglePlaces constructor
google_places = GooglePlaces(API_KEY)


def get_hospital_query_result(lat, lng):
    # Query the Google Places API
    try:
        query_result_hospital = google_places.nearby_search(
            lat_lng={'lat': lat, 'lng': lng},
            radius=5000,
            types=[types.TYPE_HOSPITAL])
    except Exception as e:
        print('Could not get hospital query result: ', e)
        return None

    query_dict = {}
    i = 0
    for place in query_result_hospital.places:
        query_dict[i] = [place.name, str(place.geo_location['lat']), str(place.geo_location['lng'])]
        i += 1

    json_hospital = json.dumps(query_dict, indent=4, ensure_ascii=False)

    return json_hospital