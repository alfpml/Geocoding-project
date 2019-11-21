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

##function to connect to MOngoDB
def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

##Function to calculate distance between two points
def getLocCoord(office):
    longitude = office['longitude']
    latitude = office['latitude']
    loc = {
        'type':'Point',
        'coordinates':[longitude, latitude]
    }
    return loc

##Search places from coordinates
def nearbysearchName(query,location,radius):
    API_key = os.getenv('key')
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    places = []
    params = {
        'rankbydistance':"",
        'location': location,
        'radius': radius,
        'name': query,
        'key': API_key
    }
    res = requests.get(endpoint_url, params = params)
    results =  json.loads(res.content)
    places.extend(results['results'])
    return places

def nearbysearchText(query,location,radius):
    API_key = os.getenv('key')
    endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    places = []
    params = {
        'location': location,
        'radius': radius,
        'query': query,
        'key': API_key
    }
    res = requests.get(endpoint_url, params = params)
    results =  json.loads(res.content)
    places.extend(results['results'])
    return places


## get location from places
def getLocation(result):
    location = []
    for i in range(len(result)):
        latitude = result[i]['geometry']['location']['lat']
        longitude = result[i]['geometry']['location']['lng']
        name = result[i]['name']
        address = result[i]['vicinity']
        loc = {
            'name': name,
            'address': address,
            'longitude': longitude,
            'latitude': latitude
        }
        location.append(loc)
    return location
