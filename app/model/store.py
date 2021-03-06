from flask_mongoengine import Pagination
from app.entity.store import Store as StoreEntity
from constants import Pages
from constants import PRED_LIST, CLASS_LIST, PRED_LIST2
from mongoengine.queryset.visitor import Q
from app.model.category import CategoryModel
from app.model.address import AddressModel
from flask import session
from utils import Utils


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
        star = None
        dis = None
        quality = 0
        for key, value in filter.items():
            if key == "classification" and value != "":
                classify = PRED_LIST[value]
            elif key == "level":
                if value=="":
                    level = "top"
                else:
                    level = value
            elif key == "categories" and value != "":
                categories = value.split(',')
            elif key == "cate_predict" and value != "":
                cates_predict = value.split(',')
            elif key == "star" and value != "" and value != 'None':
                star = float(value)
            elif key == "quality" and value != "" and value != 'None':
                quality = int(value)
            elif key == "distance" and value != "":
                dis = float(value)
        
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
        
        if classify:
            stores_sorted = stores_sorted.filter(classifications=classify)

        if categories:
            cates = [CategoryModel().objects(name_link__exact=cate)[0].id for cate in categories]
            stores_sorted = stores_sorted.filter(categories_id__in=cates)

        elif cates_predict:
            print(cates_predict)
            stores_sorted = stores_sorted.filter(category_predict__in=cates_predict)

        if star:
            stores_sorted = stores_sorted.filter(Q(stars__gt=star - 1) & Q(stars__lt=star + 0.0001))

        if level:
            print(level)
            if level == "top":
                stores_sorted = stores_sorted.filter(reviewer_quant__gt=100)
                # print(len(stores_sorted_t))
                # if len(stores_sorted_t) < 10:
                #     stores_sorted = stores_sorted
                # else:
                #     stores_sorted = stores_sorted_t
            elif level == "SS":
                print(PRED_LIST2[level][1])
                stores_sorted = stores_sorted.filter(reviewer_quant__gt=PRED_LIST2[level][1])
            else:
                print(PRED_LIST2[level])
                stores_sorted = stores_sorted.filter(Q(reviewer_quant__lte=PRED_LIST2[level][0]) & Q(reviewer_quant__gte=PRED_LIST2[level][1]))
            # elif level in (8, 12, 16, 20, 24):
            #     stores_sorted = stores_sorted.filter(
            #         Q(classification__lte=level + 0.5) & Q(classification__gt=level - 3.5))   
            # elif level == 28:
            #     stores_sorted = stores_sorted.filter(classification__gt=level - 3.5)
        if quality == 1:
            stores_sorted = stores_sorted.order_by("score_sentiment")
        else:
            stores_sorted = stores_sorted.order_by("-score_sentiment")
        
        if dis:
            # ssd = stores_sorted
            # store_sastified = []
            if dis == 1:
                R_lat = dis/110.6
                R_lng = dis/108
            elif dis == 5:
                R_lat = dis/110.8
                R_lng = dis/108.3
            elif dis == 10:
                R_lat = dis/111
                R_lng = dis/108.5
            if session['pos'] is not None:
                print("aa")
                lat_u = float(session['pos'].get('lat'))    
                lon_u = float(session['pos'].get('lng'))
            else:
                print(session["pos"])
                current_user = session['cur_user']
                if current_user.address_id:
                    userAddress = AddressModel().find_by_id(current_user.address_id.id)
                    lat_u = float(userAddress[0].latitude)
                    lon_u = float(userAddress[0].longtitude)
                else:
                    lat_u = 10.7733796 
                    lon_u = 106.6584253,17

            stores_sorted = stores_sorted.filter(Q(lat__lt=lat_u+R_lat) & Q(lat__gt=lat_u-R_lat) & Q(lng__lt=lon_u+R_lng) & Q(lng__gt=lon_u-R_lng))
            # print(lat_u+dis)
            # address_stores_filter = address_stores.filter()
            # print(address_stores_filter)
            print(stores_sorted.count())
            # for store in ssd:
            #     lat_s = float(store.address_id.latitude)
            #     lon_s = float(store.address_id.longtitude)
            #     if session['pos'] is not None:
            #         lat_u = float(session['pos'].get('lat'))
            #         lon_u = float(session['pos'].get('lng'))
            #     d = Utils.getDistanceFromLatLonInKm(lat_s, lon_s, lat_u, lon_u)
            #     if d < dis:
            #         store_sastified.append(store.id)
            # stores_sorted = stores_sorted.filter(id__in=store_sastified)
                

        # num = len(stores_sorted)
        num = 0
        stores = Pagination(stores_sorted, int(page), int(Pages['NUMBER_PER_PAGE']))
        return stores.items, stores.pages, num

    def find_by_id(self, store_id):
        return self.objects(id__exact=store_id)

    def find_by_name(self, name):
        return self.objects(name__exact=name)[0]

    def find_lst_by_name(self, name):
        return self.objects(name__exact=name)

    def find_by_categories(self, categories_id):
        lst =[]
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
            # cates = [CategoryModel().objects(id__exact=cate)[0].id for cate in categories_id]
            store_filtered = self.objects.filter(categories_id__in=categories_id)
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

    @classmethod
    def create(cls, name, description, link_image, categories_id, address_id, position, name_translate,
               category_predict, type_store, min_price, max_price, lat, lng):
        try:
            store = StoreEntity(name=name, description=description, link_image=link_image,
                                categories_id=categories_id, address_id=address_id, position=position,
                                name_translate=name_translate,
                                category_predict=category_predict, type_store=type_store,
                                min_price=min_price, max_price=max_price, lat=lat, lng=lng).save()
            StoreEntity.add_to_index_into_table(store)
            return True, None
        except Exception as e:
            return False, e.__str__()

    def count(self):
        return self.objects.count()

    def query_recent(self):
        return self.objects.order_by("created_at")

    @classmethod
    def update(cls, name, description, link_image, categories_id, store_id, address_id, min_price, max_price, position, lat, lng):
        try:
            store = StoreEntity.objects(id=store_id).get()
            store.description = description
            store.link_image = link_image
            store.address_id = address_id
            store.categories_id = categories_id
            store.min_price = min_price
            store.max_price = max_price
            store.position = position
            store.lat = lat
            store.lng = lng
            store.save()
            return True, None
        except Exception as e:
            return False, e.__str__()

    @classmethod
    def delete(cls, store_id, deleted_at):
        try:
            store = StoreEntity.objects(id=store_id).get()
            store.deleted_at = deleted_at
            store.save()
            return store, None
        except Exception as e:
            return None, e.__str__()
    