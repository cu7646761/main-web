from pymongo import MongoClient
import random
import time
from google.cloud import automl_v1beta1 as automl
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pain/Downloads/britcat2-0026abc98690.json"

PROJECT_ID = "britcat2" #@param {type:"string"}
COMPUTE_REGION = "us-central1" # Currently only supported region.

automl_client = automl.AutoMlClient()
tables_client = automl.TablesClient(project=PROJECT_ID, region=COMPUTE_REGION)

conn = MongoClient()    
db = conn['main_1']
collection = db.store
categories = db.category
all_data = collection.find()

class_list = {
    1: 'SS+', 2: 'SS', 3: 'S+', 4: 'S',
    5: 'AA+', 6: 'AA', 7: 'A+', 8: 'A',
    9: 'BB+', 10: 'BB', 11: 'B+', 12: 'B',
    13: 'CC+', 14: 'CC', 15: 'C+', 16: 'C',
    17: 'DD+', 18: 'DD', 19: 'D+', 20: 'D',
    21: 'EE+', 22: 'EE', 23: 'E+', 24: 'E',
    25: 'FF+', 26: 'FF', 27: 'F+', 28: 'F'
}

cl =['SS+','SS','S+','S',
    'AA+','AA','A+','A',
    'BB+','BB','B+','B',
    'CC+','CC','C+','C',
    'DD+','DD','D+','D',
    'EE+','EE','E+','E',
    'FF+','FF','F+','F'
]

cl_list = [
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 15, 16,
    17, 18, 19, 20,
    21, 22, 23, 24,
    25, 26, 27, 28
]

def get_name_link_by_id(oid):
    cate = categories.find({"_id": oid})
    a = loads(dumps(cate))
    return a[0]['name_link']


list_models = tables_client.list_models()
for model in list_models:
    if model.display_name == "data_training_v4__20200311045426":
        my_model = model
        break
cnt = 0
for data in all_data:
    if cnt <= 2670:
        cnt+=1
        print(cnt)
        continue
    cates = []
    for oid in data['categories_id']:
        # if len(cates) > 2:
        #     cates+= ','
        name = get_name_link_by_id(oid)
        name_cate ='[\"' + name + '\"]'
        cates.append(name_cate)

    if data['max_price'] == 'Đang cập nhật':
        max_price = -1
        cates.append("[\"\"]")
    else:
        max_price = int(data['max_price'])
    if data['min_price'] == 'Đang cập nhật':
        min_price = -1
        cates.append("[\"\"]")
    else:
        min_price = int(data['min_price'])
    if len(cates)>=2:
        prs=[]
        for cate in cates:
            inputs = {
                "Age" : -1,
                "Categories": cate,
                "Cmt_1": data['comments_s'],
                "Cmt_2": data['comments_a'],
                "Cmt_3": data['comments_b'],
                "Cmt_4": data['comments_c'],
                "Cmt_5": data['comments_d'],
                "Cmt_6": data['comments_e'],
                "Cmt_7": data['comments_f'],
                "Cmt_8": data['comments_g'],
                "Cmt_9": data['comments_h'],
                "Cmt_10": data['comments_i'],
                "Distances": -1,
                "Max_prices": max_price,
                "Min_prices": min_price,
                "Star_s1": data['star_s1'],
                "Star_s2": data['star_s2'],
                "Star_s3": data['star_s3'],
                "Star_s4": data['star_s4'],
                "Star_s5": data['star_s5']
            }
            pr = tables_client.predict(model=my_model, inputs=inputs)
            prs.append(pr.payload[0].tables.value.number_value)
        rs = sum(prs)/len(prs)
        collection.update_one({"_id": data['_id']},{"$set": {"classification": rs}})
    else:
        inputs = {
            "Age" : -1,
            "Categories": cates[0],
            "Cmt_1": data['comments_s'],
            "Cmt_2": data['comments_a'],
            "Cmt_3": data['comments_b'],
            "Cmt_4": data['comments_c'],
            "Cmt_5": data['comments_d'],
            "Cmt_6": data['comments_e'],
            "Cmt_7": data['comments_f'],
            "Cmt_8": data['comments_g'],
            "Cmt_9": data['comments_h'],
            "Cmt_10": data['comments_i'],
            "Distances": -1,
            "Max_prices": max_price,
            "Min_prices": min_price,
            "Star_s1": data['star_s1'],
            "Star_s2": data['star_s2'],
            "Star_s3": data['star_s3'],
            "Star_s4": data['star_s4'],
            "Star_s5": data['star_s5']
        }
        
        prediction_result = tables_client.predict(model=my_model, inputs=inputs)
        print(prediction_result)
        rs = prediction_result.payload[0].tables.value.number_value
        collection.update_one({"_id": data['_id']},{"$set": {"classification": rs}})

    cnt+=1
    print(cnt)
    if cnt % 50 == 0 :
        time.sleep(30)



