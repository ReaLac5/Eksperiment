import pymongo
import csv
from faker import Faker
import random

url = 'mongodb://mongo:27017/'
client = pymongo.MongoClient(url)
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

with open('MOCK_DATA.csv', 'r') as file:
    print(company_dict)
    reader = csv.DictReader(file)
    for row in reader:
        company_names = set()
        num_companies = random.randint(min_companies, max_companies)

        while len(company_names) < num_companies:
            company_name = random.choice(list(company_dict.keys()))
            if company_name not in company_names:
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
            'companies': [{'name': name, 'address': company_dict[name]} for name in company_names]
        }
        collection_person_2.insert_one(data_2)

print("Data inserted into MongoDB")
