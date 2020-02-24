from flask_mongoengine import Pagination
from app.entity.store import Store as StoreEntity
from constants import Pages


class StoreModel(StoreEntity):
    objects = StoreEntity.objects

    def get_name_by_id(self, user_id):
        return self.objects.get(id=user_id).name

    def query_all(self):
        return self.objects

    def query_paginate(self, page):
        stores = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return stores.items, stores.pages

    def query_paginate_sort(self, page):
        stores_sorted = self.objects.order_by("-classification")
        stores = Pagination(stores_sorted, int(page), int(Pages['NUMBER_PER_PAGE']))
        return stores.items, stores.pages

    def find_by_id(self, user_id):
        return self.objects(id__exact=user_id)

    def find_by_email(self, email):
        return self.objects(email__exact=email)

    def get_cate(self, categories_id):
        return ["sang-trong", "buffet"]

    # def edit(self, _id, email):
    #     try:
    #         self.objects(id__exact=_id).update(set__email=email)
    #         StoreEntity.reindex()
    #         return True, None
    #     except Exception as e:
    #         return False, e.__str__()

    @classmethod
    def create(cls, email, password):
        try:
            StoreEntity(email=email, password=password).save()
            # StoreEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()