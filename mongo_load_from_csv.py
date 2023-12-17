import pymongo
import csv
from bson import ObjectId

client = pymongo.MongoClient('mongodb://mongo:27017/')
db = client['eksperiment']
collection = db['Person']
collection_person_2 = db['Person-2']
collection_company = db['Company']
collection_person_3 = db['Person-3']
collection_person_4 = db['Person-4']
collection_company_2 = db['Company-2']

def insert_person(collection, filename):
    with open(filename, 'r') as file:
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

def insert_person_2(collection, filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            companies_str = row['companies']
            companies_list = eval(companies_str)

            companies_list = [ObjectId(company) for company in companies_list]

            data = {
                '_id': ObjectId(row['_id']),
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'companies': companies_list
            }

            collection.insert_one(data)

insert_person(collection, 'output_data_Person.csv')
print("Data inserted into MongoDB - Person")

insert_person_2(collection_person_2, 'output_data_Person_2.csv')
print("Data inserted into MongoDB - Person - 2")

insert_person(collection_person_3, 'output_data_Person_3.csv')
print("Data inserted into MongoDB - Person - 3")

insert_person_2(collection_person_4, 'output_data_Person_4.csv')
print("Data inserted into MongoDB - Person - 4")

def insert_company(collection, filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            data = {
                '_id': ObjectId(row['_id']),
                'name': row['name'],
                'address': row['address']
            }

            collection.insert_one(data)

insert_company(collection_company, 'output_data_Company.csv')
print("Data inserted into MongoDB - Company")

insert_company(collection_company_2, 'output_data_Company_2.csv')
print("Data inserted into MongoDB - Company - 2")
