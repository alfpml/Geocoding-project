from pymongo import MongoClient
import pandas as pd
import geopy.distance
import googlemaps
from datetime import datetime
import os
import requests
import json
import time
import pandas as pd
import folium
from dotenv import load_dotenv
load_dotenv()

import functions as f
import filtered_offices as off


db, coll = f.connectCollection('companies_cb','offices')

offices_2 = list(coll.find())

for i in offices_2:
    value = {"$set": {'location':f.getLocCoord(i)}}
    coll.update_one(i, value)
