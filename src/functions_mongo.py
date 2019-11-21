from pymongo import MongoClient

##function to connect to MOngoDB
def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll