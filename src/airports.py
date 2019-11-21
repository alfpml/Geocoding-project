from pymongo import MongoClient
import pandas as pd
import geopy.distance
import functions_search as fs
import functions_rank as fr
import functions_mongo as fm
import filtered_offices as off

db, coll = fm.connectCollection('companies_cb','airports')

##Creating a list of US airports with over 40 direct flights
airports = coll.find(
    {
    '$and': [
        {
            'country': 'United States'
        }, {
            'type': 'Airports'
        }
    ]
})

airports_list=list(airports)
df_airports=  pd.DataFrame(airports_list)

columns = ['tz','phone','type','email','url','runway_length','elev','_id']
df_airports.drop(columns, inplace=True, axis=1)

df_airports=df_airports.dropna(subset = ['direct_flights','carriers'])
df_airports[["direct_flights", "carriers"]] = df_airports[["direct_flights", "carriers"]].apply(pd.to_numeric)

df_airports = df_airports[df_airports.direct_flights > 40]
df_airports.reset_index(drop=True, inplace=True)

##print(len(df_airports))
##print(df_airports)
##print(df_airports.dtypes)

df_airports.to_csv("./output/filtered_airports.csv")