from flask_mongoengine import Pagination
from app.entity.mongo.address import Address as AddressEntity
from constants import Pages, Errors


class AddressModel(AddressEntity):
    objects = AddressEntity.objects

    def query_all(self):
        return self.objects

    def query_paginate(self, page):
        addresses = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return addresses.items, addresses.pages, addresses.page

    def find(self, name):
        return self.objects(name__exact=name)

    def get_name_by_id(self, address_id):
        try:
            return self.objects.get(id=address_id).detail, None
        except Exception as e:
            return None, e.__str__()

    def edit(self, _id, district_id, detail):
        try:
            self.objects(id__exact=_id).update(set__detail=detail, set__district_id=district_id)
            AddressEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()

    @classmethod
    def create(cls, district_id, detail):
        try:
            if not district_id or not detail:
                return False, Errors.ERROR_EXIST.value
            AddressEntity(detail=detail, district_id=district_id).save()
            AddressEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()
