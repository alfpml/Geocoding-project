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
##print(len(companies2))

##Creating Data Frame at office level to further filter

idt=[]
name=[]
category=[]
description=[]
city=[]
country=[]
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
        country.append(companies2[c].get('offices',0)[office].get('country_code'))
        latitude.append(companies2[c].get('offices',0)[office].get('latitude'))
        longitude.append(companies2[c].get('offices',0)[office].get('longitude'))
        year_founded.append(companies2[c].get('founded_year',0))
        employees.append(companies2[c].get('number_of_employees',0))
        total_money_raised.append(companies2[c].get('total_money_raised',0))

filtered={"idt":idt,"name":name, "category":category,"description":description,"city":city,"country":country,"latitude":latitude,"longitude":longitude,"year_founded":year_founded,"employees":employees,"total_money_raised":total_money_raised}
filtered_df=pd.DataFrame(filtered)

## Removing null/na values from capital fields (coorrds/city)
filtered=filtered_df.dropna(subset = ['latitude','longitude'])
filtered=filtered_df.dropna(subset = ['city'])
filtered=filtered[filtered['city'].notnull()]
filtered=filtered[filtered['latitude'].notnull()]
filtered=filtered[filtered['longitude'].notnull()]



##Filtering to US where most of the companies are and counting companies per city
filtered['is_gaming']  = filtered.apply(lambda x: 1 if x.category=='games_video' else 0, axis=1)
filtered['total_companies'] = filtered.groupby('city')['city'].transform('count')

filtered['gaming_companies'] = filtered.groupby('city').sum().is_gaming
print(filtered.head(20))

##Filtering out cities with high concentration of startup companies (over 50) and with too low (below 20) 
filtered2=filtered[(filtered['total_companies']>20)&(filtered['total_companies']<=50)&(filtered['country']=="USA")]
cities=filtered2['city'].value_counts()

gaming_companies=filtered2[filtered2['category']=='games_video']
cities_gaming=gaming_companies['city'].value_counts()


print(len(filtered2))
print(cities)
print(cities_gaming)

## ----> This already gives me 



##print(filtered)
##filtered2.to_csv("./output/filt_comp_coords.csv")

