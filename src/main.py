import googlemaps
import geopy.distance
from pymongo import MongoClient
from datetime import datetime
import os
import requests
import json
import time
import pandas as pd
import folium
import functions as f
from dotenv import load_dotenv
load_dotenv()

def main():
    ## 1. import filtered CSVs of candidate offices (fileterd in filtered_offices.py)
    offices=pd.read_csv("./output/filtered_offices.csv")

    ## 2. Distance to Closest Airport

        ## importing CSV with US international airports filterd in airports.py
    airports=pd.read_csv("./output/filtered_airports.csv")

        ## creating list with distance to closest airport through closest_airport function in functions.py
    dist_airport=[]
    for x in range(len(offices)):
        office=offices.iloc[x]
        dist_airport.append(f.closest_airport(office,airports))

        ## appending dist_airport to office df
    offices['dist_airport'] = dist_airport 

    ## 3. Distance to Closest Starbucks
    dist_starbucks=[]
    for x in range(len(offices)):
    office=offices.iloc[x]
    dist_starbucks.append(closest_starbucks(office))

    offices['dist_starbucks'] = dist_starbucks 

if __name__ == "__main__":
    main()