import csv
from faker import Faker

fake = Faker()

def generate_company_dict(count):
    unique_companies = {}
    while len(unique_companies) < count:
        company_name = fake.company()
        if company_name not in unique_companies:
            unique_companies[company_name] = fake.address()
    return unique_companies

company_dict = generate_company_dict(13000)

with open('company_data_2.csv', 'w', newline='') as csvfile:
    fieldnames = ['Company', 'Address']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for key, value in company_dict.items():
        writer.writerow({'Company': key, 'Address': value})