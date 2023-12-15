import pymongo
import csv
from faker import Faker
import random

url = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(url)
db = client['eksperiment']
collection = db['Person']
collection_person_2 = db['Person-2']
collection_company = db['Company']

fake = Faker()

min_companies = 2
max_companies = 5

unique_companies_global = {}

with open('MOCK_DATA.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        company_names = set()
        num_companies = random.randint(min_companies, max_companies)
        unique_companies = {}
        company_ids = {}

        while len(company_names) < num_companies:
            company_name = fake.company()

            if company_name in unique_companies_global:
                unique_companies[company_name] = unique_companies_global[company_name]
            else:
                address = fake.address()
                unique_companies[company_name] = address
                unique_companies_global[company_name] = address

                company_data = {
                    'name': company_name,
                    'address': address
                }
                inserted_company = collection_company.insert_one(company_data)
                inserted_company_id = inserted_company.inserted_id
                company_ids[company_name] = inserted_company_id

            company_names.add(company_name)

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
