from flask_mongoengine import Pagination
from app.entity.address import Address as AddressEntity
from constants import Pages
from bson import ObjectId


class AddressModel(AddressEntity):
    objects = AddressEntity.objects

    def get_name_by_id(self, address_id):
        return self.objects.get(id=address_id).name

    def query_all(self):
        return self.objects

    def query_paginate(self, page):
        addresss = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return addresss.items, addresss.pages

    def find_by_id(self, address_id):
        return self.objects(id__exact=address_id)

    def find_by_detail(self, detail):
        return self.objects(detail__exact=detail)

    def findAllById(self, listIds):
        categories = []
        for x in listIds:
            categories = categories + [self.objects(id__exact=x)]
        return categories

    @classmethod
    def create(cls, detail):
        try:
            AddressEntity(detail=detail).save()
            # UserEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()
