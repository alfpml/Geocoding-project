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


starbucks1 = f.nearbysearchName('starbucks','30.268735,-97.745209',250)
strb_df=pd.DataFrame(f.getLocation(starbucks1))

print(strb_df)
##starbucks_df.to_csv('starbucks.csv')
##starbucks1.to_csv('./output/starbucks.csv')

