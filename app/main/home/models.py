from flask_mongoengine import Pagination
from app.entity.mongo.user import User as UserEntity
from constants import Pages


class UserModel(UserEntity):
    objects = UserEntity.objects

    def get_name_by_id(self, User_id):
        return self.objects.get(id=User_id).name

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

    @classmethod
    def create(cls, email, password):
        try:
            UserEntity(email=email, password=password).save()
            UserEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()