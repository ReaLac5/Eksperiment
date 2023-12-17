from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from random import choice
from pymongo import MongoClient
import csv
import random
from bson import ObjectId
from faker import Faker


def get_Collection(name_of_collection):
    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    collection = db[name_of_collection]
    return collection

def index(requst):
    return HttpResponse("<h1>App is running</h1>")

def get_all_person(request):
    person_collection = get_Collection('Person')
    persons = person_collection.find()
    return HttpResponse(persons)


def get_all_person_2(request):
    person_collection = get_Collection('Person-2')
    persons = person_collection.find()
    return HttpResponse(persons)


def get_all_company(request):
    company_collection = get_Collection('Company')
    companies = company_collection.find()
    return HttpResponse(companies)

def get_companies_by_name(request):
    first_names = []
    with open('MOCK_DATA.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            first_names.append(row['first_name'])
 
    person_collection = get_Collection('Person')
        
    random_name = random.choice(first_names)

    person = person_collection.find_one({"first_name": random_name})

    companies = person.get("companies", [])
    
    company_list = [{"company_name": company} for company in companies]

    return JsonResponse(company_list, safe=False)


def get_companies_by_name_2(request):
    first_names = []
    with open('MOCK_DATA.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            first_names.append(row['first_name'])

    person_collection = get_Collection('Person-2')
    company_collection = get_Collection('Company')

    random_name = random.choice(first_names)

    person = person_collection.find_one({"first_name": random_name})

    company_ids = person.get("companies", [])
    
    company_names = []
    for company_id in company_ids:
        company = company_collection.find_one({"_id": ObjectId(company_id)})
        if company:
            company_names.append({"company_name": company.get("name")})

    return JsonResponse(company_names, safe=False)


def get_people_by_company_name(request):
    company_dict_read = {}
    with open('company_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_dict_read[row['Company']] = row['Address']
    
    collection = get_Collection('Person')

    random_company_name = choice(list(company_dict_read.keys()))

    people_with_company = collection.find({'companies': random_company_name}, {'_id': 0})
    
    people_names = [{'first_name': person['first_name'], 'last_name': person['last_name']} for person in people_with_company]

    return JsonResponse({'people_with_company': people_names})

def get_people_by_company_name_2(request):
    company_dict_read = {}
    with open('company_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_dict_read[row['Company']] = row['Address']
    
    person_collection = get_Collection('Person-2')
    company_collection = get_Collection('Company')

    random_company_name = choice(list(company_dict_read.keys()))

    company = company_collection.find_one({'name': random_company_name})

    company_id = company['_id']
    
    people_with_company = person_collection.find({'companies': company_id}, {'_id': 0})
    
    people_names = [{'first_name': person['first_name'], 'last_name': person['last_name']} for person in people_with_company]

    return JsonResponse({'people_with_company': people_names})

    """for person in people_list:
        company_ids = person['companies']
        company_names = []
        for company_id in company_ids:
            company = company_collection.find_one({'_id': ObjectId(company_id)})
            if company and 'name' in company:
                company_names.append(company['name'])
        person['companies'] = company_names"""


def add_company_to_person(request):
    fake = Faker()
    with open('MOCK_DATA.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        random_row = random.choice(list(reader))

    first_name = random_row['first_name']
    last_name = random_row['last_name']

    person_collection = get_Collection('Person')

    person = person_collection.find_one({"first_name": first_name, "last_name": last_name})

    if person:
        with open('company_data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            company_data = [row['Company'] for row in reader]

        while True:
            new_company_name = fake.company()
            if new_company_name not in company_data:
                break

        person_collection.update_one(
            {"first_name": first_name, "last_name": last_name},
            {"$addToSet": {"companies": new_company_name}}
        )
        return JsonResponse({"message": "Company added successfully"})
    else:
        return JsonResponse({"message": "Person not found"})


def add_company_to_person_2(request):
    fake = Faker()
    with open('MOCK_DATA.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        random_row = random.choice(list(reader))

    first_name = random_row['first_name']
    last_name = random_row['last_name']

    
    person_collection = get_Collection('Person-2')
    company_collection = get_Collection('Company')

    person = person_collection.find_one({"first_name": first_name, "last_name": last_name})

    if person:
        with open('company_data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            company_data = [row['Company'] for row in reader]

        while True:
            new_company_name = fake.company()
            if new_company_name not in company_data:
                break

        company = {
            'name': new_company_name,
        }
        company_collection.insert_one(company)

        company = company_collection.find_one({"name": new_company_name})
        if company:
            person_collection.update_one(
                {"first_name": first_name, "last_name": last_name},
                {"$addToSet": {"companies": ObjectId(company["_id"])}}
            )
        return JsonResponse({"message": "Company added successfully"})
    else:
        return JsonResponse({"message": "Person not found"})


def update_companies(request):
    fake = Faker()

    company_names = []
    with open('companies.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_names.append(row['Company'])

    old_company_name = random.choice(company_names)

    person_collection = get_Collection('Person')

    persons_to_update = person_collection.find({'companies': old_company_name})

    while True:
        new_company_name = fake.company()
        if new_company_name not in company_names:
            break

    for person in persons_to_update:
        updated_companies = [new_company_name if company == old_company_name else company for company in person['companies']]
        person_collection.update_one(
            {'_id': person['_id']},
            {'$set': {'companies': updated_companies}}
        )

def update_companies_2(request):
    fake = Faker()

    company_names = []
    with open('companies.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            company_names.append(row['Company'])

    old_company_name = random.choice(company_names)

    while True:
        new_company_name = fake.company()
        if new_company_name not in company_names:
            break

    company_collection = get_Collection('Company')

    company_collection.update_one({'name': old_company_name}, {'$set': {'name': new_company_name}})

