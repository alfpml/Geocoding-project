from pymongo import MongoClient

def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

db, coll = connectCollection('companies_cb','companies_cb')


companies = coll.find(
{
    'deadpooled_year': {
        '$exists': True
    }
},
{
    'deadpooled_year': None
}
)

companies2=list(companies)
print(len(companies2))


