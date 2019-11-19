from pymongo import MongoClient

def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

db, coll = connectCollection('companies_cb','companies_cb')

##find companies with more than 50 employees or having funding rounds

companies = coll.find(
{
    '$or': [
        {
            '$and': [
                {
                    'number_of_employees': None
                },{
                    'funding_rounds.raised_amount': {
                        '$gt': 250000
                    }
                },{
                    'founded_year':{'$gte': 2003}
                }
            ]
        }, 
        {
            '$and': [
        
        
        {
            'number_of_employees': {
                '$gt': 50
            }}
        ,{
            'founded_year':{'$gte': 2003}
            }
        ]
        }
    ]
}
)

companies2=list(companies)
print(len(companies2))


