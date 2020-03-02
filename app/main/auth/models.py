from flask_mongoengine import Pagination
from app.entity.user import User as UserEntity
from constants import Pages


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

    def update_basic(self, email, birthday=None, gender=None, favorite_categories=None, address_id=None):
        try:
            self.objects(email__exact=email).update(set__birthday=birthday)
            self.objects(email__exact=email).update(set__gender=gender)
            self.objects(email__exact=email).update(set__favorite_categories=favorite_categories)
            self.objects(email__exact=email).update(set__address_id=address_id)
            return True, None
        except Exception as e:
            return False, e.__str__()

    def update_psw(self, email, psw):
        try:
            self.objects(email__exact=email).update(set__password=psw)
            return True, None
        except Exception as e:
            return False, e.__str__()

    def update_link_image(self, email, link_image):
        try:
            self.objects(email__exact=email).update(set__link_image=link_image)
            # UserEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()

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