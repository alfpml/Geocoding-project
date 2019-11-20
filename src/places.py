import googlemaps
from pymongo import MongoClient
from datetime import datetime
import os
import requests
import json
import time
import pandas as pd
import folium
from dotenv import load_dotenv
load_dotenv()

##Search places from coordinates
def searchPlaces(query, location):
    API_key = os.getenv('key')
    endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    places = []
    params = {
        'query': query,
        'location': location,
        'radius': 0.25,
        'key': API_key
    }
    res = requests.get(endpoint_url, params = params)
    results =  json.loads(res.content)
    places.extend(results['results'])
    time.sleep(2)
    while "next_page_token" in results:
        params['pagetoken'] = results['next_page_token'],
        res = requests.get(endpoint_url, params = params)
        results = json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
    return places

## get location from places
def getLocation(result):
    location = []
    for i in range(len(result)):
        latitude = result[i]['geometry']['location']['lat']
        longitude = result[i]['geometry']['location']['lng']
        name = result[i]['name']
        address = result[i]['formatted_address']
        loc = {
            'name': name,
            'address': address,
            'longitude': longitude,
            'latitude': latitude
        }
        location.append(loc)
    return location
