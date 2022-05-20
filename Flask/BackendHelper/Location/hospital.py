from flask import jsonify
from googleplaces import GooglePlaces, types, lang
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Google Places API
API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')

# Initialising the GooglePlaces constructor
google_places = GooglePlaces(API_KEY)


def get_hospital_query_result(lat, lng):
    # Query the Google Places API
    try:
        query_result_hospital = google_places.nearby_search(
            lat_lng={'lat': lat, 'lng': lng},
            types=[types.TYPE_HOSPITAL],
            rankby='distance',
            keyword='Public Hospital',
            language='de'
        )
        return query_result_hospital
    except Exception as e:
        print('Could not get hospital query result: ', e)
        return e

    query_dict = {}
    i = 0
    for place in query_result_hospital.places:
        #query_dict[i] = [place.name, str(place.geo_location['lat']), str(place.geo_location['lng'])]
        query_dict[i] = {
            'name': place.name,
            'latitude': place.geo_location['lat'],
            'longitude': place.geo_location['lng']
        }
        i += 1

    json_hospital = jsonify(query_dict)

    return json_hospital