import googlemaps
from pymongo import MongoClient
from datetime import datetime
import os
import requests
import json
import time
import pandas as pd
import folium
import geopy.distance
from dotenv import load_dotenv
load_dotenv()

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

def nearbysearchType(query,location,radius,gtype):
    API_key = os.getenv('key')
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    places = []
    params = {
        'rankbydistance':"",
        'location': location,
        'radius': radius,
        'query': query,
        'type':gtype,
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

##Function to find closest airport
def closest_airport(office,df):
    coords_off = (office.get('latitude'),office.get('longitude'))
    dist = []
    for i in range(len(df)):
        coords_air = (df.iloc[i].get('lat'),df.iloc[i].get('lon'))
        dist.append(geopy.distance.geodesic(coords_off, coords_air).km)
    return min(dist)


##Function to find closest starbucks
def closest_starbucks(office):
    coords_off = (office.get('latitude'),office.get('longitude'))
    coords_off2 = ("{},{}".format(coords_off[0],coords_off[1]))
    nbs_list=nearbysearchName("starbucks",coords_off2,1000)
    dist = []
    a=0
    if nbs_list==[]:
        dist.append(a)
    else:
        starbucks=pd.DataFrame(getLocation(nbs_list)).iloc[0]
        coords_str=(starbucks.get('latitude'),starbucks.get('longitude'))
        geo_dist=(geopy.distance.geodesic(coords_off, coords_str).m)
        dist.append(geo_dist)
        return dist[0]

##Function to find closest vegan
def closest_gtype(office,query,radius,gtype):
    coords_off = (office.get('latitude'),office.get('longitude'))
    coords_off2 = ("{},{}".format(coords_off[0],coords_off[1]))
    nbs_list=nearbysearchType(query,coords_off2,radius,gtype)
    dist = []
    a=0
    if nbs_list==[]:
        dist.append(a)
    else:
        df=pd.DataFrame(getLocation(nbs_list)).iloc[0]
        coords_df=(df.get('latitude'),df.get('longitude'))
        geo_dist=(geopy.distance.geodesic(coords_off, coords_df).m)
        dist.append(geo_dist)
    return dist[0]