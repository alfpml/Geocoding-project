from pymongo import MongoClient
import pandas as pd
import geopy.distance


##function to connect to MOngoDB
def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

##Function to calculate distance between two points
def getLocCoord(office):
    longitude = office['longitude']
    latitude = office['latitude']
    loc = {
        'type':'Point',
        'coordinates':[longitude, latitude]
    }
    return loc



db, coll = connectCollection('companies_cb','offices')

offices_2 = list(coll.find())

for i in offices_2:
    value = {"$set": {'location':getLocCoord(i)}}
    coll.update_one(i, value)




