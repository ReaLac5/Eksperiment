from django.shortcuts import render
from .models import person_collection
from django.http import HttpResponse
from mongo_loader import company_dict
from random import choice

from django.http import JsonResponse
import random

def index(requst):
    return HttpResponse("<h1>App is running</h1>")

def add_person(request):
    records = {
        "first_name": "John",
        "last_name": "Smith"
    }
    person_collection.insert_one(records)
    return HttpResponse("New person is added")


def get_all_person(request):
    persons = person_collection.find()
    return HttpResponse(persons)




from django.http import JsonResponse
from pymongo import MongoClient
import random

def get_random_names(request):
    # Connect to your MongoDB
    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']  # Assuming 'eksperiment' is the database name
    collection = db['Person']  # Assuming 'Person' is the collection name

    # Retrieve a random document from the 'Person' collection
    random_document = collection.aggregate([{ '$sample': { 'size': 1 } }])

    # Extract relevant data from the random document
    if random_document:
        random_data = list(random_document)[0]  # Get the first (and only) document

        # Extract fields from the document
        first_name = random_data.get('first_name')
        last_name = random_data.get('last_name')
        companies = random_data.get('companies', [])

        # Prepare the response as JSON
        response_data = {
            'first_name': first_name,
            'last_name': last_name,
            'companies': companies,
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'No records found'}, status=404)
    

def get_random_names_2(request):
    # Connect to your MongoDB
    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']  # Assuming 'eksperiment' is the database name
    collection = db['Person-2']  # Assuming 'Person' is the collection name

    # Retrieve a random document from the 'Person' collection
    random_document = collection.aggregate([{ '$sample': { 'size': 1 } }])

    # Extract relevant data from the random document
    if random_document:
        random_data = list(random_document)[0]  # Get the first (and only) document

        # Extract fields from the document
        first_name = random_data.get('first_name')
        last_name = random_data.get('last_name')
        companies = random_data.get('companies', [])

        # Prepare the response as JSON
        response_data = {
            'first_name': first_name,
            'last_name': last_name,
            'companies': companies,
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'No records found'}, status=404)



def get_company_name_by_id(company_id, company_collection):
    company = company_collection.find_one({'_id': company_id})
    return company['name'] if company else None

def get_people_by_company(request):
    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    collection = db['Person']

    random_company_name = choice(list(company_dict.keys()))

    # Query the MongoDB collection for people with the random company name
    people_with_company = collection.find({'companies': random_company_name}, {'_id': 0})

    people_list = list(people_with_company)

    return JsonResponse(people_list, safe=False)


def get_people_by_company_2(request):
    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    collection_2 = db['Person-2']
    company_collection = db['Company']

    random_company_name = choice(list(company_dict.keys()))

    company = company_collection.find_one({'company_name': random_company_name})
    company_id = company['_id']

    people_with_company = person_collection.find({'companies': company_id}, {'_id': 0})

    people_list = list(people_with_company)

    return JsonResponse(people_list, safe=False)