from pymongo import MongoClient
import pandas as pd
import geopy.distance

def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

def distance(coord_1,coord_2):
return geopy.distance.vincenty(coords_1, coords_2).km