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
import functions_search as fs
import functions_rank as fr
import functions_mongo as fm
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
        dist_airport.append(fs.closest_airport(office,airports))

        ## appending dist_airport to office df
    offices['dist_airport'] = dist_airport 

    ## 3. Distance to Closest Starbucks
    dist_starbucks=[]
    for x in range(len(offices)):
        office=offices.iloc[x]
        dist_starbucks.append(fs.closest_starbucks(office))

    offices['dist_starbucks'] = dist_starbucks

    ## 4. Distance to Closest Vegan Restaurant
    dist_vegan=[]
    for x in range(len(offices)):
        office=offices.iloc[x]
        dist_vegan.append(fs.closest_gtype(office,"vegan",500,"restaurant"))

    offices['dist_vegan'] = dist_vegan

    ## 5. Distance to Closest Waldorf school
    dist_school=[]
    for x in range(len(offices)):
        office=offices.iloc[x]
        dist_school.append(fs.closest_gtype(office,"waldorf",10000,"school"))

    offices['dist_school'] = dist_school


    ## 6. Building Rank
    offices['rank'] = offices.apply (lambda row: fr.rank_airport(row), axis=1) + offices.apply (lambda row: fr.rank_starbucks(row), axis=1) + offices.apply (lambda row: fr.rank_vegan(row), axis=1) + offices.apply (lambda row: fr.rank_schools(row), axis=1)
    offices=offices.sort_values('rank',ascending=False)
    
    ## 7. Printing most suitable location
    print(offices.iloc[0])

    map_office=folium.Map(location=[37.4864,-122.23],zoom_start=30)


map_office

if __name__ == "__main__":
    main()