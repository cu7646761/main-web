from flask_mongoengine import Pagination
from app.entity.store import Store as StoreEntity
from constants import Pages
from bson import ObjectId
from constants import PRED_LIST, CLASS_LIST
from mongoengine.queryset.visitor import Q
from app.main.category.models import CategoryModel

class StoreModel(StoreEntity):
    objects = StoreEntity.objects

    def get_name_by_id(self, store_id):
        return self.objects.get(id=store_id).name

    def query_all(self):
        return self.objects

    def query_paginate(self, page):
        stores = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return stores.items, stores.pages

    def query_paginate_sort(self, page, filter):
        classify = None
        level = None
        categories = None
        for key, value in filter.items():
            if key == "classification" and value != "":
                classify = PRED_LIST[value]
            elif key == "level" and value != "":
                level = PRED_LIST[value]
            elif key == "categories" and value != "":
                categories = value.split(',')

        stores_sorted = self.objects.order_by("classification")

        if level:
            if level == 2:
                stores_sorted = stores_sorted.filter(classification__lte=2)
            elif level == 4:
                stores_sorted = stores_sorted.filter(Q(classification__lte=4) & Q(classification__gt=2))
            elif level in (8, 12, 16, 20, 24, 28):
                stores_sorted = stores_sorted.filter(Q(classification__lte=level) & Q(classification__gt=level-4))

        elif classify:
            stores_sorted = stores_sorted.filter(classifications=classify)

        if categories:
            cates = [CategoryModel().objects(name_link__exact=cate)[0].id for cate in categories]
            stores_sorted = stores_sorted.filter(categories_id__in=cates)
        
        stores = Pagination(stores_sorted, int(page), int(Pages['NUMBER_PER_PAGE']))
        return stores.items, stores.pages

    def find_by_id(self, store_id):
        return self.objects(id__exact=store_id)

    def find_by_name(self, name):
        return self.objects(name__exact=name)[0]

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