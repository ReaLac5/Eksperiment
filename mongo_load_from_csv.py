import pymongo
import csv
from bson import ObjectId

url = 'mongodb://mongo:27017/'
client = pymongo.MongoClient(url)
db = client['eksperiment']
collection = db['Person']
collection_person_2 = db['Person-2']
collection_company = db['Company']

with open('output_data_Person.csv', 'r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        companies_str = row['companies']
        companies_list = eval(companies_str)

        data = {
            '_id': ObjectId(row['_id']),
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'companies': companies_list
        }

        collection.insert_one(data)

print("Data inserted into MongoDB")

with open('output_data_Person_2.csv', 'r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        companies_str = row['companies']

        companies_list_str = eval(companies_str)
        #companies_list = [ObjectId(company.strip().replace("ObjectId('", '').replace("')", '')) for company in companies_list_str]
        companies_list = [ObjectId(company) for company in companies_list_str]

        data = {
            '_id': ObjectId(row['_id']),
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'companies': companies_list
        }

        collection_person_2.insert_one(data)

print("Data inserted into MongoDB")

with open('output_data_Company.csv', 'r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        data = {
            '_id': ObjectId(row['_id']),
            'name': row['name'],
            'address': row['address']
        }

        collection_company.insert_one(data)

print("Data inserted into MongoDB")
