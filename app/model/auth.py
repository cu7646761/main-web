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

    def update_basic(self, email, birthday=None, gender=None, favorite_categories=None):
        try:
            self.objects(email__exact=email).update(set__birthday=birthday)
            self.objects(email__exact=email).update(set__gender=gender)
            self.objects(email__exact=email).update(set__favorite_categories=favorite_categories)
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
            user = UserEntity(email=email, password=password, active=active).save()
            # UserEntity.add_to_index_into_table(user)
            return True, None
        except Exception as e:
            return False, e.__str__()

    # def trigger_user_store_rel(self, uid):
    #     stores = StoreEntity.objects
    #     usrel = USRelEntity.objects
    #     for store in stores:
    #         classify = 1 + 2
    #         usrel.create(uid, store.id, classify)

    def count(self):
        return self.objects.count()

    def query_recent(self):
        return self.objects.order_by("created_at")

    def changeStatus(self, id, active):
        try:
            self.objects(id__exact=id).update(set__active=active)
            return True, None
        except Exception as e:
            return False, e.__str__()

    def delete(self, user_id):
        try:
            user = UserEntity.objects(id=user_id).get()
            user.delete()
            user.save()
            return
        except Exception as e:
            return False, e.__str__()
