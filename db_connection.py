import pymongo
import csv

url = 'mongodb://mongo:27017/'
client = pymongo.MongoClient(url)

db = client['eksperiment']
