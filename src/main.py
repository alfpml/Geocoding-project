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
        
        ## Getting Closest Starbucks to draw it into the map
    starbucks=fs.nearbysearchName("starbucks","{},{}".format(office1['latitude'],office1['longitude']),500)
    closest_starbucks=pd.DataFrame(fs.getLocation(starbucks)).iloc[0]
    coords_starbucks=(closest_starbucks.get('latitude'),closest_starbucks.get('longitude'))
    print(coords_starbucks)


        ## Getting Closest Vegan to draw it into the map
    vegans=fs.nearbysearchType("vegan","{},{}".format(office1['latitude'],office1['longitude']),500,"restaurant")
    closest_vegan=pd.DataFrame(fs.getLocation(vegans)).iloc[0]
    coords_vegan=(closest_vegan.get('latitude'),closest_vegan.get('longitude'))
    print(coords_vegan)

        ## Getting Closest Waldorf School to draw it into the map
    schools=fs.nearbysearchType("waldorf school","{},{}".format(office1['latitude'],office1['longitude']),500,"school")
    closest_school=pd.DataFrame(fs.getLocation(schools)).iloc[0]
    coords_school=(closest_school.get('latitude'),closest_school.get('longitude'))
    print(coords_school)

        ##printing map with markers for closest starbucks, vegan and school
    map_office=folium.Map(location=[office1['latitude'],office1['longitude']],zoom_start=20)

    folium.Marker([office1['latitude'],office1['longitude']],radius=2,icon=folium.Icon(icon='pushpin',color='black'),popup='Office',).add_to(map_office)
    folium.Marker(coords_starbucks,radius=2,icon=folium.Icon(icon='cloud',color='green'),popup='Starbucks',).add_to(map_office)
    folium.Marker(coords_vegan,radius=2,icon=folium.Icon(icon='cutlery',color='red'),popup='Vegan',).add_to(map_office)
    folium.Marker(coords_school,radius=2,icon=folium.Icon(icon='baby-formula',color='blue'),popup='School',).add_to(map_office)

    def embed_map(m, file_name):
        from IPython.display import IFrame
        m.save(file_name)
        return IFrame(file_name, width='100%', height='500px')  
        
    embed_map(map_office,"./output/office_location.html")

    map_office

if __name__ == "__main__":
    main()