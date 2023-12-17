import pymongo
import csv

client = pymongo.MongoClient('mongodb://mongo:27017/')
db = client['eksperiment']
collection = db['Person']
collection_person_2 = db['Person-2']
collection_company = db['Company']

csv_file_path = 'output_data_Person.csv'
csv_file_path_2 = 'output_data_Person_2.csv'
csv_file_path_3 = 'output_data_Company.csv'

def export_to_csv(cursor, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        first_document = next(cursor, None)
        if first_document:
            headers = list(first_document.keys())
            csv_writer.writerow(headers)

            csv_writer.writerow(first_document.values())

            for document in cursor:
                csv_writer.writerow(document.values())

def export_data_to_csv():
    export_to_csv(collection.find(), csv_file_path)
    print(f"Data has been exported to '{csv_file_path}'")

    export_to_csv(collection_person_2.find(), csv_file_path_2)
    print(f"Data has been exported to '{csv_file_path_2}'")

    export_to_csv(collection_company.find(), csv_file_path_3)
    print(f"Data has been exported to '{csv_file_path_3}'")

export_data_to_csv()
