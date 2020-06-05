from flask_mongoengine import Pagination
from app.entity.store import Store as StoreEntity
from constants import Pages
from bson import ObjectId
from constants import PRED_LIST, CLASS_LIST, PRED_LIST2
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
        cates_predict = None
        for key, value in filter.items():
            if key == "classification" and value != "":
                classify = PRED_LIST[value]
            elif key == "level":
                if value == "":
                    level = "top"
                else:
                    level = value
            elif key == "categories" and value != "":
                categories = value.split(',')
            elif key == "cate_predict" and value != "":
                cates_predict = value.split(',')

        stores_sorted = self.objects

        # if level:
        #     if level == 2:
        #         stores_sorted = stores_sorted.filter(classification__lte=2.5)
        #     elif level == 4:
        #         stores_sorted = stores_sorted.filter(Q(classification__lte=4.5) & Q(classification__gt=2.5))
        #     elif level in (8, 12, 16, 20, 24):
        #         stores_sorted = stores_sorted.filter(
        #             Q(classification__lte=level + 0.5) & Q(classification__gt=level - 3.5))
        #     elif level == 28:
        #         stores_sorted = stores_sorted.filter(classification__gt=level - 3.5)

        if level:
            print(level)
            if level == "top":
                stores_sorted = stores_sorted.filter(reviewer_quant__gt=200)
            elif level == "SS":
                print(PRED_LIST2[level][1])
                stores_sorted = stores_sorted.filter(reviewer_quant__gt=PRED_LIST2[level][1])
            else:
                stores_sorted = stores_sorted.filter(
                    Q(reviewer_quant__lte=PRED_LIST2[level][0]) & Q(reviewer_quant__gte=PRED_LIST2[level][1]))
            # elif level in (8, 12, 16, 20, 24):
            #     stores_sorted = stores_sorted.filter(
            #         Q(classification__lte=level + 0.5) & Q(classification__gt=level - 3.5))   
            # elif level == 28:
            #     stores_sorted = stores_sorted.filter(classification__gt=level - 3.5)

        elif classify:
            stores_sorted = stores_sorted.filter(classifications=classify)

        if categories:
            cates = [CategoryModel().objects(name_link__exact=cate)[0].id for cate in categories]
            stores_sorted = stores_sorted.filter(categories_id__in=cates)

        if cates_predict:
            print(cates_predict)
            stores_sorted = stores_sorted.filter(category_predict__in=cates_predict)

        stores_sorted = stores_sorted.order_by("-score_sentiment")
        stores = Pagination(stores_sorted, int(page), int(Pages['NUMBER_PER_PAGE']))
        return stores.items, stores.pages

    def find_by_id(self, store_id):
        return self.objects(id__exact=store_id)

    def find_by_name(self, name):
        return self.objects(name__exact=name)[0]

    def find_by_categories(self, categories_id):
        lst = []
        for x in self.objects:
            if categories_id == x.categories_id:
                lst = lst + [x]
        return lst

    def find_optimize_by_categories(self, category, categories_id, page, store_id):
        # lst =[]
        # count = 0
        # end = 0
        if category != 'other':
            store_filtered = self.objects(category_predict__exact=category)
        else:
            cates = [CategoryModel().objects(id__exact=cate)[0].id for cate in categories_id]
            store_filtered = self.objects.filter(categories_id__in=cates)
        store_filtered = store_filtered.filter(reviewer_quant__gt=200)
        store_filtered = store_filtered.filter(id__ne=store_id)
        stores_sorted = store_filtered.order_by("score_sentiment")
        stores = Pagination(stores_sorted, int(page), 6)

        return stores.items, stores.pages
        # for x in self.objects[begin:]:
        #     end += 1  
        #     if categories_id == x.categories_id:
        #         lst = lst + [x]
        #         count += 1
        #     if count == 6:
        #         break
        # print(begin)
        # print(end)
        # return lst, end

    # def edit(self, _id, email):
    #     try:
    #         self.objects(id__exact=_id).update(set__email=email)
    #         StoreEntity.reindex()
    #         return True, None
    #     except Exception as e:
    #         return False, e.__str__()

    @classmethod
    def create(cls, name, description, link_image, categories_id, address_id):
        try:
            StoreEntity(name=name, description=description, link_image=link_image, categories_id=categories_id,
                        address_id=address_id).save()
            # StoreEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()

    def count(self):
        return self.objects.count()

    def query_recent(self):
        return self.objects.order_by("created_at")

    @classmethod
    def update(cls, name, description, link_image, categories_id, store_id, address_id):
        try:
            store = StoreEntity.objects(id=store_id).get()
            store.description = description
            store.link_image = link_image
            store.address_id = address_id
            store.categories_id = categories_id
            store.save()
            return True, None
        except Exception as e:
            return False, e.__str__()

    @classmethod
    def delete(cls, store_id, deleted_at):
        try:
            store = StoreEntity.objects(id=store_id).get()
            print(store.name)
            store.deleted_at = deleted_at
            store.save()
            return store, None
        except Exception as e:
            return False, e.__str__()
