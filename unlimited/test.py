import sys
import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://%s:%s@localhost:27017' %
                     ("clarity", "clarity#demo"))

db = client["clarity-data"]
collection = db["hosts"]


def delete_many():
    collection.delete_many({})


def find():
    r = collection.find({})
    for c in r:
        print(c)


find()
delete_many()
