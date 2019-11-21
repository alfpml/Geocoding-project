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

starbucks1 = f.nearbysearchName('starbucks','30.268735,-97.745209',250)
strb_df=pd.DataFrame(f.getLocation(starbucks1))

print(strb_df)
print(strb_df.iloc[0])
print(type(strb_df.iloc[0]))

##starbucks_df.to_csv('starbucks.csv')
##starbucks1.to_csv('./output/starbucks.csv')
