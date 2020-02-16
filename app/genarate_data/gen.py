import csv
import os
import random

import pymongo
from bson import ObjectId
from pymongo import MongoClient
from random import randint

# Step 1: Connect to MongoDB - Note: Change connection string as needed
client = MongoClient(port=27017)
db = client.crud_1

# Step 2: Create sample data
# names = []
# with open(os.path.abspath(os.path.dirname(__file__)) + '/city.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             names.append(row[0])
#             line_count += 1
#     print(f'Processed {line_count} lines.')
# print(names)
# for x in range(1, 1000):
#     business = {
#         '_cls': 'City',
#         'name': names[x]
#     }
#     #Step 3: Insert business object directly into MongoDB via isnert_one
#     try:
#         result= db.city.insert_one(business)
#     except pymongo.errors.DuplicateKeyError:
#         # skip document because it already exists in new collection
#         continue
#     #Step 4: Print to the console the ObjectID of the new document
#     print('Created {0} of 1000 as {1}'.format(x,result.inserted_id))
# #Step 5: Tell us that you are done
# print('finished creating 1000 cities')


# names = []
# with open(os.path.abspath(os.path.dirname(__file__)) + '/district.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             names.append(row[0])
#             line_count += 1
#     print(f'Processed {line_count} lines.')
# print(names)
# for x in range(1, 1000):
#     # print("id of city:", db.city.find()[x]['_id'])
#     business = {
#         '_cls': 'District',
#         'name': names[x],
#         'city_id': db.city.find()[x]['_id']
#     }
#     #Step 3: Insert business object directly into MongoDB via isnert_one
#     try:
#         result = db.district.insert_one(business)
#     except pymongo.errors.DuplicateKeyError:
#         # skip document because it already exists in new collection
#         continue
#     # Step 4: Print to the console the ObjectID of the new document
#     print('Created {0} of 1000 as {1}'.format(x, result.inserted_id))
# #Step 5: Tell us that you are done
# print('finished creating 1000 districts')


# names = []
# with open(os.path.abspath(os.path.dirname(__file__)) + '/address.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             names.append(row[0])
#             line_count += 1
#     print(f'Processed {line_count} lines.')
# print(names)
# for x in range(1, 1000):
#     # print("id of city:", db.city.find()[x]['_id'])
#     business = {
#         '_cls': 'Address',
#         'detail': names[x],
#         'district_id': db.district.find()[x]['_id']
#     }
#     # Step 3: Insert business object directly into MongoDB via isnert_one
#     try:
#         result = db.address.insert_one(business)
#     except pymongo.errors.DuplicateKeyError:
#         # skip document because it already exists in new collection
#         continue
#     # Step 4: Print to the console the ObjectID of the new document
#     print('Created {0} of 1000 as {1}'.format(x, result.inserted_id))
# #Step 5: Tell us that you are done
# print('finished creating 1000 addresses')


# names = []
# with open(os.path.abspath(os.path.dirname(__file__)) + '/store.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             names.append(row[0])
#             line_count += 1
#     print(f'Processed {line_count} lines.')
# print(names)
# for x in range(1, 1000):
#     # print("id of city:", db.city.find()[x]['_id'])
#     business = {
#         '_cls': 'Store',
#         'store_name': names[x],
#         'address_id': db.address.find()[x]['_id']
#     }
#     # Step 3: Insert business object directly into MongoDB via isnert_one
#     try:
#         result = db.store.insert_one(business)
#     except pymongo.errors.DuplicateKeyError:
#         # skip document because it already exists in new collection
#         continue
#     # Step 4: Print to the console the ObjectID of the new document
#     print('Created {0} of 1000 as {1}'.format(x, result.inserted_id))
# #Step 5: Tell us that you are done
# print('finished creating 1000 stores')


# names = []
# with open(os.path.abspath(os.path.dirname(__file__)) + '/color.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             names.append(row[0])
#             line_count += 1
#     print(f'Processed {line_count} lines.')
# print(names)
# for x in range(1, 1000):
#     business = {
#         '_cls': 'Color',
#         'value': names[x]
#     }
#     # Step 3: Insert business object directly into MongoDB via isnert_one
#     try:
#         result = db.color.insert_one(business)
#     except pymongo.errors.DuplicateKeyError:
#         # skip document because it already exists in new collection
#         business['value'] = business['value'] + " " + str(random.randint(0, 60000))
#         print(business['value'])
#         result = db.color.insert_one(business)
#
#     # Step 4: Print to the console the ObjectID of the new document
#     print('Created {0} of 1000 as {1}'.format(x, result.inserted_id))
# #Step 5: Tell us that you are done
# print('finished creating 1000 colors')


# names = []
# with open(os.path.abspath(os.path.dirname(__file__)) + '/brand.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             names.append(row[0])
#             line_count += 1
#     print(f'Processed {line_count} lines.')
# print(names)
# for x in range(1, 1000):
#     business = {
#         '_cls': 'Brand',
#         'name': names[x]
#     }
#     # Step 3: Insert business object directly into MongoDB via isnert_one
#     try:
#         result = db.brand.insert_one(business)
#     except pymongo.errors.DuplicateKeyError:
#         # skip document because it already exists in new collection
#         business['name'] = business['name'] + " " + str(random.randint(0, 60000))
#         result = db.brand.insert_one(business)
#
#     # Step 4: Print to the console the ObjectID of the new document
#     print('Created {0} of 1000 as {1}'.format(x, result.inserted_id))
# #Step 5: Tell us that you are done
# print('finished creating 1000 brands')


# names = []
# with open(os.path.abspath(os.path.dirname(__file__)) + '/category.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             names.append(row[0])
#             line_count += 1
#     print(f'Processed {line_count} lines.')
# print(names)
# for x in range(1, 1000):
#     business = {
#         '_cls': 'Category',
#         'name': names[x],
#         'brand_id': db.brand.find()[x]['_id']
#     }
#     # Step 3: Insert business object directly into MongoDB via isnert_one
#     try:
#         result = db.category.insert_one(business)
#     except pymongo.errors.DuplicateKeyError:
#         # skip document because it already exists in new collection
#         business['name'] = business['name'] + " " + str(random.randint(0, 60000))
#         result = db.category.insert_one(business)
#
#     # Step 4: Print to the console the ObjectID of the new document
#     print('Created {0} of 1000 as {1}'.format(x, result.inserted_id))
# #Step 5: Tell us that you are done
# print('finished creating 1000 categories')


# names = []
# with open(os.path.abspath(os.path.dirname(__file__)) + '/product.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             names.append(row[0])
#             line_count += 1
#     print(f'Processed {line_count} lines.')
# print(names)
# for x in range(1, 1000):
#     business = {
#         '_cls': 'Product',
#         'name': names[x],
#         'category_id': db.category.find()[x]['_id']
#     }
#     # Step 3: Insert business object directly into MongoDB via isnert_one
#     try:
#         result = db.product.insert_one(business)
#     except pymongo.errors.DuplicateKeyError:
#         # skip document because it already exists in new collection
#         business['name'] = business['name'] + " " + str(random.randint(0, 60000))
#         result = db.product.insert_one(business)
#
#     # Step 4: Print to the console the ObjectID of the new document
#     print('Created {0} of 1000 as {1}'.format(x, result.inserted_id))
# #Step 5: Tell us that you are done
# print('finished creating 1000 products')


names = []
with open(os.path.abspath(os.path.dirname(__file__)) + '/variant.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            names.append(row[0])
            line_count += 1
    print(f'Processed {line_count} lines.')
print(names)
for x in range(1, 1000):
    business = {
        '_cls': 'ProductVariant',
        'price': names[x],
        'product_id': db.product.find()[x]['_id'],
        'store_id': db.store.find()[x]['_id'],
        'color_id': db.color.find()[x]['_id']
    }
    # Step 3: Insert business object directly into MongoDB via isnert_one
    try:
        result = db.product_variant.insert_one(business)
    except pymongo.errors.DuplicateKeyError:
        # skip document because it already exists in new collection
        business['name'] = business['name'] + " " + str(random.randint(0, 60000))
        result = db.product_variant.insert_one(business)

    # Step 4: Print to the console the ObjectID of the new document
    print('Created {0} of 1000 as {1}'.format(x, result.inserted_id))
# Step 5: Tell us that you are done
print('finished creating 1000 product_variant')
