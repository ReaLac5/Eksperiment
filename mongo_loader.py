import pymongo
import csv
from faker import Faker
import random

client = pymongo.MongoClient('mongodb://mongo:27017/')
db = client['eksperiment']
collection = db['Person']
collection_person_2 = db['Person-2']
collection_company = db['Company']
collection_person_3 = db['Person-3']
collection_company_2 = db['Company-2']

fake = Faker()

min_companies = 2
max_companies = 5

company_dict = {}
company_dict_2 = {}

with open('company_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        company_name = row['Company']
        address = row['Address']
        
        company_dict[company_name] = address

with open('company_data_2.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        company_name = row['Company']
        address = row['Address']
        
        company_dict_2[company_name] = address

for company_name, address in company_dict.items():
    company_data = {
        'name': company_name,
        'address': address
    }
    inserted_company = collection_company.insert_one(company_data)

for company_name, address in company_dict_2.items():
    company_data = {
        'name': company_name,
        'address': address
    }
    inserted_company = collection_company_2.insert_one(company_data)


with open('MOCK_DATA.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        company_names = set()
        num_companies = random.randint(min_companies, max_companies)
        company_ids = {}

        while len(company_names) < num_companies:
            company_name = random.choice(list(company_dict.keys()))
            if company_name not in company_names:
                company_names.add(company_name)
        
        for company_name in company_names:
            company_data = collection_company.find_one({'name': company_name})
            if company_data:
                company_ids[company_name] = company_data['_id']

        data = {
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'companies': list(company_names)
        }
        collection.insert_one(data)

        data_2 = {
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'companies': [company_ids[name] for name in company_names if name in company_ids]
        }
        collection_person_2.insert_one(data_2)


print("Data inserted into MongoDB")

with open('names_10000.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        company_names = set()
        num_companies = random.randint(min_companies, max_companies)
        company_ids = {}

        while len(company_names) < num_companies:
            company_name = random.choice(list(company_dict_2.keys()))
            if company_name not in company_names:
                company_names.add(company_name)
        
        for company_name in company_names:
            company_data = collection_company_2.find_one({'name': company_name})
            if company_data:
                company_ids[company_name] = company_data['_id']

        data = {
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'companies': list(company_names)
        }
        collection_person_3.insert_one(data)

print("Data inserted into MongoDB")