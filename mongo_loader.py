import pymongo
import csv
from faker import Faker
import random

client = pymongo.MongoClient('mongodb://mongo:27017/')
db = client['eksperiment']
collection = db['Person']
collection_person_2 = db['Person-2']
collection_company = db['Company']

fake = Faker()

def generate_company_dict(count):
    unique_companies = {}
    while len(unique_companies) < count:
        company_name = fake.company()
        if company_name not in unique_companies:
            unique_companies[company_name] = fake.address()
    return unique_companies

min_companies = 2
max_companies = 5

company_dict = generate_company_dict(3000)


for company_name, address in company_dict.items():
    company_data = {
        'name': company_name,
        'address': address
    }
    inserted_company = collection_company.insert_one(company_data)


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

with open('company_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['Company', 'Address']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for key, value in company_dict.items():
        writer.writerow({'Company': key, 'Address': value})  # Adjust the field names based on your dictionary structure

print("Data inserted into MongoDB")
