from pymongo import MongoClient
import pandas as pd
import geopy.distance

def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

db, coll = connectCollection('companies_cb','airports')

##find companies with more than 50 employees or having funding rounds

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

columns = ['tz','phone','type','email','url','runway_length','elev']
df_airports.drop(columns, inplace=True, axis=1)

df_airports=df_airports.dropna(subset = ['direct_flights','carriers'])
df_airports[["direct_flights", "carriers"]] = df_airports[["direct_flights", "carriers"]].apply(pd.to_numeric)

df_airports = df_airports[df_airports.direct_flights > 40]

print(len(df_airports))
print(df_airports)
print(df_airports.dtypes)

df_airports.to_csv("./output/filtered_airports.csv")