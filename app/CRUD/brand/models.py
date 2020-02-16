from flask_mongoengine import Pagination
from app.entity.mongo.brand import Brand as BrandEntity
from constants import Pages


class BrandModel(BrandEntity):
    objects = BrandEntity.objects

    def get_name_by_id(self, brand_id):
        return self.objects.get(id=brand_id).name

    def query_all(self):
        return self.objects

    def query_paginate(self, page):
        cities = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return cities.items, cities.pages

    def find(self, name):
        return self.objects(name__exact=name)

    def find_by_id(self, brand_id):
        return self.objects(id__exact=brand_id)

    def edit(self, _id, name):
        try:
            self.objects(id__exact=_id).update(set__name=name)
            BrandEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()

    @classmethod
    def create(cls, name):
        try:
            BrandEntity(name=name).save()
            BrandEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()