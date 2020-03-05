from flask_mongoengine import Pagination
from app.entity.user import User as UserEntity
from constants import Pages
from app.entity.user_store_rel import as USRelEntity
from app.entity.store import Store as StoreEntity


class UserModel(UserEntity):
    objects = UserEntity.objects

    def get_name_by_id(self, user_id):
        return self.objects.get(id=user_id).name

    def query_all(self):
        return self.objects

    def query_paginate(self, page):
        users = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return users.items, users.pages

    def find_by_id(self, user_id):
        return self.objects(id__exact=user_id)

    def find_by_email(self, email):
        return self.objects(email__exact=email)

    # def edit(self, _id, email):
    #     try:
    #         self.objects(id__exact=_id).update(set__email=email)
    #         UserEntity.reindex()
    #         return True, None
    #     except Exception as e:
    #         return False, e.__str__()

    def turn_on_acc(self, email):
        try:
            self.objects(email__exact=email).update(set__active=1)
            # UserEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()

    @classmethod
    def create(cls, email, password, active):
        try:
            UserEntity(email=email, password=password, active=active).save()
            # UserEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()

    def trigger_user_store_rel(self, uid):
        stores = StoreEntity.objects
        usrel = USRelEntity.objects
        for store in stores:
            classify = 1+2
            usrel.create(uid, store.id, classify)
            
        