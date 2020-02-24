from flask_mongoengine import Pagination
from app.entity.store import Store as StoreEntity
from constants import Pages
from bson import ObjectId

class StoreModel(StoreEntity):
    objects = StoreEntity.objects

    def get_name_by_id(self, store_id):
        return self.objects.get(id=store_id).name

    def query_all(self):
        print(StoreEntity.objects)
        return self.objects

    def query_paginate(self, page):
        stores = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return stores.items, stores.pages

    def find_by_id(self, store_id):
        return self.objects(id__exact=store_id)


    # def edit(self, _id, email):
    #     try:
    #         self.objects(id__exact=_id).update(set__email=email)
    #         StoreEntity.reindex()
    #         return True, None
    #     except Exception as e:
    #         return False, e.__str__()

    @classmethod
    def create(cls, name, description):
        try:
            StoreEntity(name=name, description=description).save()
            # StoreEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()