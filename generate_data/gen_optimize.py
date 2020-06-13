import csv
import datetime
import os
from pymongo import MongoClient
import json
from bson.json_util import dumps
from bson.json_util import loads

# client = MongoClient(
#     'mongodb+srv://hoangan11:hoangan11123456@cluster0-ypawj.gcp.mongodb.net/foodblog1?retryWrites=true&w=majority')
# db = client.foodblog1
from app.entity.address import Address

client = MongoClient(
    'mongodb+srv://admin:britcat@clusteroptimize-wysnm.gcp.mongodb.net/test?retryWrites=true&w=majority')
db_new = client.foodblog_opt1

conn2 = MongoClient(
    'mongodb+srv://hoangan:hoangan123456@cluster0-ypawj.gcp.mongodb.net/foodblog1?retryWrites=true&w=majority')
db_old = conn2['foodblog1']

# --------- Create category ----------
# names = []
# names_link = []
# with open(os.path.abspath(os.path.dirname(__file__)) + '/category.csv', encoding="utf8") as csv_file:
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
data_old = db_old.store.find()
data_test = [data_old[0]]
for store_old in data_test:
    address_old = db_old.address.find({'_id': store_old['address_id']})[0]
    address = {
        '_cls': 'Address',
        'detail': address_old['detail'],
        'latitude': address_old['latitude'],
        'longtitude': address_old['longtitude'],
        'district': address_old['district']
    }
    address_new = db_new.address.insert_one(address)
    # address_new = None

    categories_id_new = []
    for cates in store_old['categories_id']:
        categories_id_old = db_old.category.find({'_id': cates})[0]
        category_new = db_new.category.find({'name': categories_id_old['name']})
        categories_id_new.append(category_new)

    store = {
        '_cls': 'Store',
        'name': store_old['name'],
        'name_translate': store_old['name_translate'],
        'min_price': store_old['min_price'],
        'max_price': store_old['max_price'],
        'star_s1': store_old['star_s1'],
        'star_s2': store_old['star_s1'],
        'star_s3': store_old['star_s1'],
        'star_s4': store_old['star_s1'],
        'star_s5': store_old['star_s1'],
        'stars': store_old['stars'],
        'reviewer_quant': store_old['reviewer_quant'],
        'link_image': store_old['link_image'],
        'description': store_old['description'],
        'type_store': store_old['type_store'],
        'classification': store_old['classification'],
        'score_sentiment': store_old['score_sentiment'],
        'fixed': store_old['fixed'],
        'entity_score': store_old['entity_score'],
        'position': store_old['position'],
        'category_predict': store_old['category_predict'],
        'created_at': datetime.datetime.now,
        'updated_on': None,
        'deleted_at': None,

        'address_id': address_new,
        'categories_id': categories_id_new
    }
    print(store)
    res_store = db_new.store.insert_one(store)

    # if each['address'].find(", Quận ") == -1:
    #     district = None
    # else:
    #     str_1 = each['address'][each['address'].find(", Quận ") + 1:]
    #     if str_1.find(",") == -1:
    #         district = str_1.strip()
    #     else:
    #         district = str_1[:str_1.find(",")].strip()
    #
    # address = {
    #     '_cls': 'Address',
    #     'detail': each['address'],
    #     'latitude': json.loads(each['location'])['lat'],
    #     'longtitude': json.loads(each['location'])['long'],
    #     'district': district
    # }
    #
    # res_address = db.address.insert_one(address)
    # store['address_id'] = res_address.inserted_id
    #
    # categories_id = []
    # for cate in json.loads(each['categories'])['item']:
    #     new_cate = db.category.find({"name_link": cate})
    #     categories_id.append(loads(dumps(new_cate))[0]['_id'])
    # store['categories_id'] = categories_id
    #
    # res_store = db.store.insert_one(store)
    # store_new_id = res_store.inserted_id
    #
    # comment_list_id = []
    # for cmt in each['comment_list']:
    #     comment_1 = {
    #         '_cls': 'Comment',
    #         'detail': cmt['comment'],
    #         'star_num': int(json.dumps(cmt['star_num']['$numberInt']).replace('"', "")),
    #         'store_id': store_new_id,
    #         'cus_name': cmt['author']
    #     }
    #     res_cmt = db.comment.insert_one(comment_1)
    #     comment_list_id.append(res_cmt.inserted_id)
    # if store['name'] == data_2[dem]['name']:
    #     classification = data_2[dem]['classification']
    #     entity_dict = data_2[dem]['entity_score']
    # else:
    #     break
    # update_store = db.store.update_one({"comment_list": None, "_id": store_new_id},
    #                                    {"$set":
    #                                        {
    #                                            "comment_list": comment_list_id,
    #                                            "_id": store_new_id,
    #                                            "classification": classification,
    #                                            "entity_score": entity_dict
    #                                        }
    #                                    })
    #
    # print('Created {0}'.format(each['name']))
    # dem += 1

# # --------- Add link foody to store ----------
# data_link = []
# with open(os.path.abspath(os.path.dirname(__file__)) + '/foody_link.json', encoding="utf8") as f:
#     for line in f:
#         data_link.append(json.loads(line))
#
# for each in data_link:
#     _store = db.store.find({"name": each['name']})
#     try:
#         if _store:
#             link_gg = loads(dumps(_store))[0]['link_image']
#             new_list = each['link_list']
#             new_list.insert(0, link_gg[0])
#             update_store = db.store.update_one({"name": each['name'], "link_image": link_gg},
#                                                {"$set": {"name": each['name'], "link_image": new_list}})
#     except:
#         continue
