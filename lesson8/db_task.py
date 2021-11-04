# Requires the PyMongo package.
# https://api.mongodb.com/python/current
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)


task4 = {'from_username': ''}
task5 = {'$and': [{'from_username': 'python.learning'},
                        {'user_status': 'following'}]}

iter1 = client['instagram']['instagramfollowers'].find(filter=task5)
iter2 = client['instagram']['instagramfollowers'].find(filter=task5)

for item in iter1:
    pprint(item)

for item in iter2:
    pprint(item)
