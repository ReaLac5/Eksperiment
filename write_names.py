from faker import Faker
import csv

fake = Faker()

def generate_name_dict(count):
    names = {}
    while len(names) < count:
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"
        if full_name not in names.values():
            names[first_name] = last_name
    return names

names = generate_name_dict(1500)

with open('names_10000.csv', 'w', newline='') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for key, value in names.items():
        writer.writerow({'first_name': key, 'last_name': value})