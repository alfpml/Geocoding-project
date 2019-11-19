from pymongo import MongoClient
import pandas as pd

def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

db, coll = connectCollection('companies_cb','filtered_companies')

##find companies with more than 50 employees or having funding rounds

cities = db.coll.aggregate([
		{"$group" : {"city":"$city"}}
	])

cities2=list(cities)
print(len(cities2))

