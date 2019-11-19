from pymongo import MongoClient
import pandas as pd

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


idt=[]
name=[]
category=[]
description=[]
city=[]
latitude=[]
longitude=[]
year_founded=[]
employees=[]
total_money_raised=[]

for c in range(len(companies2)):
    for office in range(len(companies2[c].get('offices',0))):
        idt.append(companies2[c].get('_id',0))
        name.append(companies2[c].get('name',0))
        category.append(companies2[c].get('category_code',0))
        description.append(companies2[c].get('description',0))
        city.append(companies2[c].get('offices',0)[office].get('city'))
        latitude.append(companies2[c].get('offices',0)[office].get('latitude'))
        longitude.append(companies2[c].get('offices',0)[office].get('longitude'))
        year_founded.append(companies2[c].get('founded_year',0))
        employees.append(companies2[c].get('number_of_employees',0))
        total_money_raised.append(companies2[c].get('total_money_raised',0))

filtered={"idt":idt,"name":name, "category":category,"description":description,"city":city,"latitude":latitude,"longitude":longitude,"year_founded":year_founded,"employees":employees,"total_money_raised":total_money_raised}
filtered_df=pd.DataFrame(filtered)
filtered=filtered_df.dropna(subset = ['city','latitude','longitude'])
filtered=filtered_df.dropna(subset = ['city'])

city_counts=filtered['city'].value_counts()
print(city_counts.head(20))


print(len(filtered))
print(filtered.head(10))
filtered.to_csv("./output/filt_comp_coords.csv")


##companies having raised over a million dollars