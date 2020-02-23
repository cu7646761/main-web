import csv
import os
from pymongo import MongoClient
import json
from bson.json_util import dumps
from bson.json_util import loads

client = MongoClient(port=27017)
db = client.main_1

# --------- Create category ----------
# names = []
# names_link = []
# with open(os.path.abspath(os.path.dirname(__file__)) + '/category.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             names.append(row[0])
#             names_link.append(row[1])
#             line_count += 1
#     print(f'Processed {line_count} lines.')
# for x in range(0, 14):
#     cate = {
#         '_cls': 'Category',
#         'name': names[x],
#         'name_link': names_link[x]
#     }
#     try:
#         result = db.category.insert_one(cate)
#     except:
#         continue
#     print('Created {0}'.format(x))
#
# print('finished create category')

# --------- Create store ----------
data = []
with open(os.path.abspath(os.path.dirname(__file__)) + '/store_json.json') as f:
    for line in f:
        data.append(json.loads(line))

for each in data:
    if each['price'] == "Đang cập nhật":
        min_price = max_price = "Đang cập nhật"
    else:
        str_price = each['price'].replace("đ", "").replace(" ", "").replace(".", "")
        min_price = str_price.split("-")[0]
        max_price = str_price.split("-")[1]

    stars = None
    try:
        stars = float(json.dumps(each['stars']['$numberDouble']).replace('"', ""))
    except:
        stars = float(json.dumps(each['stars']['$numberInt']).replace('"', ""))

    store = {
        '_cls': 'Store',
        'name': each['name'],
        'min_price': min_price,
        'max_price': max_price,
        'star_s1': int(json.dumps(each['star1s']['$numberInt']).replace('"', "")),
        'star_s2': int(json.dumps(each['star2s']['$numberInt']).replace('"', "")),
        'star_s3': int(json.dumps(each['star3s']['$numberInt']).replace('"', "")),
        'star_s4': int(json.dumps(each['star4s']['$numberInt']).replace('"', "")),
        'star_s5': int(json.dumps(each['star5s']['$numberInt']).replace('"', "")),
        'stars': stars,
        'comments_s': int(json.dumps(each['comments_s']['$numberInt']).replace('"', "")),
        'comments_a': int(json.dumps(each['comments_a']['$numberInt']).replace('"', "")),
        'comments_b': int(json.dumps(each['comments_b']['$numberInt']).replace('"', "")),
        'comments_c': int(json.dumps(each['comments_c']['$numberInt']).replace('"', "")),
        'comments_d': int(json.dumps(each['comments_d']['$numberInt']).replace('"', "")),
        'comments_e': int(json.dumps(each['comments_e']['$numberInt']).replace('"', "")),
        'comments_f': int(json.dumps(each['comments_f']['$numberInt']).replace('"', "")),
        'comments_g': int(json.dumps(each['comments_g']['$numberInt']).replace('"', "")),
        'comments_h': int(json.dumps(each['comments_h']['$numberInt']).replace('"', "")),
        'comments_i': int(json.dumps(each['comments_i']['$numberInt']).replace('"', "")),
        'reviewer_quant': int(json.dumps(each['reviewer_quant']['$numberInt']).replace('"', "")),
        'link_image': [json.dumps(each['link_image']).replace('"', "")],
        "comment_list": None
    }

    if each['address'].find(", Quận ") == -1:
        district = None
    else:
        str_1 = each['address'][each['address'].find(", Quận ") + 1:]
        if str_1.find(",") == -1:
            district = str_1.strip()
        else:
            district = str_1[:str_1.find(",")].strip()

    address = {
        '_cls': 'Address',
        'detail': each['address'],
        'latitude': json.loads(each['location'])['lat'],
        'longtitude': json.loads(each['location'])['long'],
        'district': district
    }

    res_address = db.address.insert_one(address)
    store['address_id'] = res_address.inserted_id

    categories_id = []
    for cate in json.loads(each['categories'])['item']:
        new_cate = db.category.find({"name_link": cate})
        categories_id.append(loads(dumps(new_cate))[0]['_id'])
    store['categories_id'] = categories_id

    res_store = db.store.insert_one(store)
    store_new_id = res_store.inserted_id

    comment_list_id = []
    for cmt in each['comment_list']:
        comment_1 = {
            '_cls': 'Comment',
            'detail': json.dumps(cmt['comment'])[1:-1],
            'star_num': int(json.dumps(cmt['star_num']['$numberInt']).replace('"', "")),
            'store_id': store_new_id,
            'cus_name': json.dumps(cmt['author'])[1:-1]
        }
        res_cmt = db.comment.insert_one(comment_1)
        comment_list_id.append(res_cmt.inserted_id)
    update_store = db.store.update_one({"comment_list": None, "_id": store_new_id}, {"$set": {"comment_list": comment_list_id, "_id": store_new_id}})

    print('Created {0}'.format(each['name']))
