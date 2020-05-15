import csv
import os

import pymongo
from pymongo import MongoClient
import json
from bson.json_util import dumps
from bson.json_util import loads
client = MongoClient('mongodb+srv://hoangan:hoangan123456@cluster0-ypawj.gcp.mongodb.net/foodblog1?retryWrites=true&w=majority')
db = client.foodblog1

conn = MongoClient('mongodb://localhost:27017/main_1')
db2 = conn['main_1']

# --------- Create category ----------
emails = []
passwords = []
with open(os.path.abspath(os.path.dirname(__file__)) + '/user-1000-type5.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            emails.append(row[0])
            passwords.append(row[1])
            line_count += 1
    print(f'Processed {line_count} lines.')
for x in range(0, 999):
    print(emails[x] + "|" + passwords[x])
    user_1 = {
        '_cls': 'User',
        'email': emails[x],
        'password': passwords[x]
    }
    print("create " + str(x))
    try:
        result = db.user.insert_one(user_1)
    except:
        continue


print('finished create user')