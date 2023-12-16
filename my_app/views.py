from django.shortcuts import render
from .models import person_collection
from django.http import HttpResponse
#from mongo_loader import company_dict
from random import choice

import csv

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
    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    person_collection = db['Person-2']
    company_collection = db['Company']
    persons = person_collection.find()
    return HttpResponse(persons)



from django.http import JsonResponse
from pymongo import MongoClient
import random

def get_random_names(request):
    company_dict_read = {}
    with open('company_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_dict_read[row['Company']] = row['Address']
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

def get_people_by_company(request, selected_company):
    #company_dict_read = {}
    #with open('company_data.csv', newline='') as csvfile:
        #reader = csv.DictReader(csvfile)
        #for row in reader:
            #company_dict_read[row['Company']] = row['Address']
    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    collection = db['Person']

    #random_company_name = choice(list(company_dict_read.keys()))

    people_with_company = collection.find({'companies': selected_company}, {'_id': 0})
    
    people_list = list(people_with_company)

    return render(request, 'people_list.html', {'people_list': people_list})

    #return JsonResponse(people_list, safe=False)

def get_people_by_company_name(request):
    company_dict_read = {}
    with open('company_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_dict_read[row['Company']] = row['Address']
    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    collection = db['Person']

    random_company_name = choice(list(company_dict_read.keys()))

    people_with_company = collection.find({'companies': random_company_name}, {'_id': 0})
    
    people_list = list(people_with_company)

    return JsonResponse(people_list, safe=False)

def get_people_by_company_name_2(request):
    company_dict_read = {}
    with open('company_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_dict_read[row['Company']] = row['Address']
    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    person_collection = db['Person-2']
    company_collection = db['Company']

    random_company_name = choice(list(company_dict_read.keys()))

    company = company_collection.find_one({'name': random_company_name})
    company_id = company['_id']

    #company_id = company.get('_id')
    
    people_with_company = person_collection.find({'companies': company_id}, {'_id': 0})
    
    people_list = list(people_with_company)

    """for person in people_list:
        company_ids = person['companies']
        company_names = []
        for company_id in company_ids:
            company = company_collection.find_one({'_id': ObjectId(company_id)})
            if company and 'name' in company:
                company_names.append(company['name'])
        person['companies'] = company_names"""

    return JsonResponse(people_list, safe=False)


from bson import ObjectId 
from django.http import HttpResponseServerError
def get_people_by_company_2(request, selected_company):
    #company_dict_read = {}
    #with open('company_data.csv', newline='') as csvfile:
        #reader = csv.DictReader(csvfile)
        #for row in reader:
            #company_dict_read[row['Company']] = row['Address']
    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    person_collection = db['Person-2']
    company_collection = db['Company']

    #random_company_name = choice(list(company_dict_read.keys()))

    company = company_collection.find_one({'name': selected_company})
    #company_id = company['_id']
    if company:
        company_id = company.get('_id')
        
        people_with_company = person_collection.find({'companies': company_id}, {'_id': 0})
        
        people_list = list(people_with_company)
        for person in people_list:
            company_ids = person['companies']
            company_names = []
            for company_id in company_ids:
                company = company_collection.find_one({'_id': ObjectId(company_id)})
                if company and 'name' in company:
                    company_names.append(company['name'])
            person['companies'] = company_names
        
        return render(request, 'people_list_2.html', {'people_list': people_list})
    else:
        return HttpResponseServerError('Company not found')
    #return JsonResponse(people_list, safe=False)


from django.shortcuts import render

def select_company(request):
    company_dict = {}
    with open('company_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_dict[row['Company']] = row['Address']

    if request.method == 'POST':
        selected_company = request.POST.get('company')
        
        selected_company_address = company_dict[selected_company]
        # Assuming get_people_by_company retrieves relevant person data
        return get_people_by_company(request, selected_company)

    return render(request, 'select_company.html', {'company_dict': company_dict})

def select_company_2(request):
    company_dict = {}
    with open('company_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_dict[row['Company']] = row['Address']

    if request.method == 'POST':
        selected_company = request.POST.get('company')
        
        selected_company_address = company_dict[selected_company]
        # Assuming get_people_by_company retrieves relevant person data
        return get_people_by_company_2(request, selected_company)

    return render(request, 'select_company_2.html', {'company_dict': company_dict})



from django.shortcuts import render
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId

def update_companies(request):
    if request.method == 'POST':
        # Handling form submission
        person_id = request.POST.get('person_id')
        companies = request.POST.get('companies').split(',') if request.POST.get('companies') else []

        client = MongoClient('mongodb://mongo:27017/')
        db = client['eksperiment']
        people_collection = db['Person']

        if person_id:
            try:
                #updated_companies = companies.split(', ')  # Assuming companies are comma-separated
                people_collection.update_one(
                    {'_id': ObjectId(person_id)},
                    {'$set': {'companies': companies}}
                )
                return HttpResponse('Companies updated successfully!')
            except Exception as e:
                return HttpResponseServerError(f'Error: {str(e)}')
        else:
            return HttpResponseServerError('Please provide a valid person ID!')
    else:
        # Fetching data for the dropdown
        try:
            client = MongoClient('mongodb://mongo:27017/')
            db = client['eksperiment']
            person_collection = db['Person']

            people_list = list(person_collection.find({}, {'_id': 1, 'companies': 1}))
            print(people_list)
            people_dropdown = [{'id': str(person['_id']), 'companies': person.get('companies', [])} for person in people_list]
            
            return render(request, 'update_companies.html', {'people_list': people_dropdown})
        except Exception as e:
            return HttpResponseServerError(f'Error: {str(e)}')


def update_companies_2(request):
    if request.method == 'POST':
        # Handling form submission
        person_id = request.POST.get('person_id')
        new_company_name = request.POST.get('companies')

        client = MongoClient('mongodb://mongo:27017/')
        db = client['eksperiment']
        people_collection = db['Person']
        company_collection = db['Company']

        if person_id and new_company_name:
            try:
                # Find the person
                person = people_collection.find_one({'_id': ObjectId(person_id)})
                if person:
                    # Update company name in the company collection
                    company_ids = person.get('companies', [])
                    for company_id in company_ids:
                        company_collection.update_one(
                            {'_id': company_id},
                            {'$set': {'name': new_company_name}}
                        )
                    return HttpResponse('Company name updated successfully!')
                else:
                    return HttpResponseServerError('Person not found!')
            except Exception as e:
                return HttpResponseServerError(f'Error: {str(e)}')
        else:
            return HttpResponseServerError('Please provide a valid person ID and new company name!')
    else:
        # Fetching data for the dropdown
        try:
            client = MongoClient('mongodb://mongo:27017/')
            db = client['eksperiment']
            person_collection = db['Person']

            people_list = list(person_collection.find({}, {'_id': 1, 'companies': 1}))
            people_dropdown = [{'id': str(person['_id'])} for person in people_list]
            
            return render(request, 'update_companies_2.html', {'people_list': people_dropdown})
        except Exception as e:
            return HttpResponseServerError(f'Error: {str(e)}')





from django.http import JsonResponse
from pymongo import MongoClient

def list_people_in_company(request):
    # Connecting to the database
    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    person_collection = db['Person']

    company_dict = {}
    with open('company_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_dict[row['Company']] = row['Address']

    # Company name for which you want to retrieve employees
    company_name = random.choice(list(company_dict.keys()))

    # Retrieving people working in the selected company
    people_in_company = person_collection.find({'companies': company_name})

    
    people_names = [{'first_name': person['first_name'], 'last_name': person['last_name']} for person in people_in_company]

    return JsonResponse({'people_in_company': people_names})


def list_people_in_company_2(request):
    # Connecting to the database
    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    person_collection = db['Person-2']
    company_collection = db['Company']

    company_dict = {}
    with open('company_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_dict[row['Company']] = row['Address']

    # Company name for which you want to retrieve employees
    company_name = random.choice(list(company_dict.keys()))

    # Get the ObjectId of the selected company from the Company collection
    company = company_collection.find_one({'name': company_name})

    company_id = company['_id']

    # Retrieving people working in the selected company by searching for company_id in the 'companies' list
    people_in_company = person_collection.find({'companies': company_id})

    # Creating a list with the names of people
    people_names = [{'first_name': person['first_name'], 'last_name': person['last_name']} for person in people_in_company]

    # Returning the result as a JSON response
    return JsonResponse({'people_in_company': people_names})


def get_companies_by_name(request):
    first_names = []
    with open('MOCK_DATA.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            first_names.append(row['first_name'])
        
    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    collection = db['Person']
        
    random_name = random.choice(first_names)

    # Now, use the random name to search in the Person collection in MongoDB
    person = person_collection.find_one({"first_name": random_name})

    companies = person.get("companies", [])
    
    company_list = [{"name": company} for company in companies]

    return JsonResponse(company_list, safe=False)


def get_companies_by_name_2(request):
    first_names = []
    with open('MOCK_DATA.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            first_names.append(row['first_name'])

    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    person_collection = db['Person-2']
    company_collection = db['Company']

    random_name = random.choice(first_names)

    # Now, use the random name to search in the Person collection in MongoDB
    person = person_collection.find_one({"first_name": random_name})

    company_ids = person.get("companies", [])
    
    company_names = []
    for company_id in company_ids:
        company = company_collection.find_one({"_id": ObjectId(company_id)})
        if company:
            company_names.append({"name": company.get("name")})

    return JsonResponse(company_names, safe=False)

from faker import Faker

def add_company_to_person(request):
    fake = Faker()
    with open('MOCK_DATA.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        random_row = random.choice(list(reader))

    first_name = random_row['first_name']
    last_name = random_row['last_name']

    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    person_collection = db['Person']

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

    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    person_collection = db['Person-2']
    company_collection = db['Company']

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




def update_companies_new_2(request):
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

    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    company_collection = db['Company']

    company_collection.update_many({'name': old_company_name}, {'$set': {'name': new_company_name}})


def update_companies_new(request):
    fake = Faker()

    company_names = []
    with open('companies.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_names.append(row['Company'])

    old_company_name = random.choice(company_names)

    client = MongoClient('mongodb://mongo:27017/')
    db = client['eksperiment']
    person_collection = db['Person']

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
