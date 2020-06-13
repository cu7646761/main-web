from flask_mongoengine import Pagination
from app.entity.address import Address as AddressEntity
from app.entity.user import User as UserEntity
from constants import Pages


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
    def create(cls, user_id, detail, district, latitude, longtitude):
        try:
            address = AddressEntity(detail=detail, district=district, latitude=latitude, longtitude=longtitude)
            address.save()
            user = UserEntity.objects(id=user_id).get()
            user.address_id = address.id
            user.save()
            # UserEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()

    @classmethod
    def create_store(cls, detail, district, latitude, longtitude):
        try:
            address = AddressEntity(detail=detail, district=district, latitude=latitude, longtitude=longtitude)
            address.save()
            # UserEntity.reindex()
            return address.id, None
        except Exception as e:
            return None, e.__str__()

    @classmethod
    def update(cls, address_id, detail, district, latitude, longtitude):
        try:
            address = AddressEntity.objects(id=address_id).get()
            address.detail = detail
            address.district = district
            address.latitude = latitude
            address.longtitude = longtitude
            address.save()
            return address, None
        except Exception as e:
            return False, e.__str__()
