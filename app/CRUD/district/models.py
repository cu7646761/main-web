from flask_mongoengine import Pagination
from app.entity.mongo.district import District as DistrictEntity
from constants import Pages


class DistrictModel(DistrictEntity):
    objects = DistrictEntity.objects

    def query_paginate(self, page):
        districts = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return districts.items, districts.pages

    def find(self, name):
        return self.objects(name__exact=name)

    def find_by_id(self, district_id):
        return self.objects(id__exact=district_id)

    def query_by_city_id(self, city_id):
        return self.objects(city_id__exact=city_id)

    def edit(self, _id, name, city_id):
        try:
            self.objects(id__exact=_id).update(set__name=name, set__city_id=city_id)
            DistrictEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()

    @classmethod
    def create(cls, name, city_id):
        try:
            DistrictEntity(name=name, city_id=city_id).save()
            DistrictEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()
