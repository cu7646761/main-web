from flask_mongoengine import Pagination
from app.entity.mongo.store import Store as StoreEntity
from constants import Pages, Errors


class StoreModel(StoreEntity):
    objects = StoreEntity.objects

    def query_paginate(self, page):
        stores = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return stores.items, stores.pages

    def query_all(self):
        return self.objects

    def find(self, store_name):
        return self.objects(store_name__exact=store_name)

    def edit(self, _id, store_name, address_id):
        try:
            self.objects(id__exact=_id).update(set__store_name=store_name, set__address_id=address_id)
            StoreEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()

    @classmethod
    def create(cls,  store_name, address_id):
        try:
            if not address_id or not store_name:
                return False, Errors.ERROR_EXIST.value
            StoreEntity(store_name=store_name, address_id=address_id).save()
            StoreEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()