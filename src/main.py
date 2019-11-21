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
        dist_starbucks.append(f.closest_starbucks(office))

    offices['dist_starbucks'] = dist_starbucks

    ## 4. Distance to Closest Vegan Restaurant
    dist_vegan=[]
    for x in range(len(offices)):
        office=offices.iloc[x]
        dist_vegan.append(closest_gtype(office,"vegan",500,"restaurant"))

    offices['dist_vegan'] = dist_vegan

    ## 5. Distance to Closest Waldorf school
    dist_school=[]
    for x in range(len(offices)):
        office=offices.iloc[x]
        dist_school.append(closest_gtype(office,"waldorf",10000,"school"))

    offices['dist_school'] = dist_school


    ## 6. Building Rank

    def rank(row):
        if row['dist_airport']==1:
            return 'Hispanic'
        if row['dist_starbucks']
            return 'Two Or More'
        if row['dist_airport']==1:
            return 'A/I AK Native'
        if row['eri_asian']==1:
            return 'Asian'
        if row['eri_afr_amer']==1:
            return 'Black/AA'
        if row['eri_hawaiian']== 1:
            return 'Haw/Pac Isl.'
        if row['eri_white']==1:
            return 'White'
        return 'Other'

if __name__ == "__main__":
    main()