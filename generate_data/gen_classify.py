from pymongo import MongoClient
import random

conn = MongoClient()
db = conn['main_1']
collection = db.store
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

cl = ['SS+', 'SS', 'S+', 'S',
      'AA+', 'AA', 'A+', 'A',
      'BB+', 'BB', 'B+', 'B',
      'CC+', 'CC', 'C+', 'C',
      'DD+', 'DD', 'D+', 'D',
      'EE+', 'EE', 'E+', 'E',
      'FF+', 'FF', 'F+', 'F'
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
for data in all_data:
    collection.update_one({"_id": data['_id']}, {"$set": {"classification": random.choice(cl_list)}})
