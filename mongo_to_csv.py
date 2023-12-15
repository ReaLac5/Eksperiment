import pymongo
import csv
import pandas as pd

url = 'mongodb://mongo:27017/'
client = pymongo.MongoClient(url)
db = client['eksperiment']
collection = db['Person']
collection_person_2 = db['Person-2']
collection_company = db['Company']

cursor = collection.find()
cursor_person_2 = collection_person_2.find()
cursor_company = collection_company.find()

csv_file_path = 'output_data_Person.csv'
csv_file_path_2 = 'output_data_Person_2.csv'
csv_file_path_3 = 'output_data_Company.csv'

with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    first_document = next(cursor, None)
    if first_document:
        headers = list(first_document.keys())
        csv_writer.writerow(headers)

        # Write the first document's values to the CSV file
        csv_writer.writerow(first_document.values())

        # Write remaining documents' values to the CSV file
        for document in cursor:
            csv_writer.writerow(document.values())

print(f"Data has been exported to '{csv_file_path}'")

with open(csv_file_path_2, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    first_document = next(cursor_person_2, None)
    if first_document:
        headers = list(first_document.keys())
        csv_writer.writerow(headers)

        # Write the first document's values to the CSV file
        csv_writer.writerow(first_document.values())

        # Write remaining documents' values to the CSV file
        for document in cursor_person_2:
            csv_writer.writerow(document.values())

print(f"Data has been exported to '{csv_file_path_2}'")

with open(csv_file_path_3, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    first_document = next(cursor_company, None)
    if first_document:
        headers = list(first_document.keys())
        csv_writer.writerow(headers)

        # Write the first document's values to the CSV file
        csv_writer.writerow(first_document.values())

        # Write remaining documents' values to the CSV file
        for document in cursor_company:
            csv_writer.writerow(document.values())

print(f"Data has been exported to '{csv_file_path_3}'")
