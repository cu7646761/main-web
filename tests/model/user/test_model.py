from app.entity.user import User as UserEntity
from app.model.auth import UserModel
from tests.test_client import FlaskClientTestCase
from utils import Utils


class UserTestCase(FlaskClientTestCase):

    def test_update_psw(self):
        user = UserModel()
        hashed_passwd = Utils.hash_password("123")
        user_1 = UserEntity.objects(email__exact='phuongvuong1998@gmail.com')[0]
        print(user_1.password)
        new, err = user.update_psw('phuongvuong1998@gmail.com', str(hashed_passwd))
        user_1 = UserEntity.objects(email__exact='phuongvuong1998@gmail.com')[0]
        print(new)
        print(err)
        print(user_1)
        print(UserEntity.objects.all())
        print(Utils.check_password("123", user_1.password))
        self.assertTrue(Utils.check_password("123", user_1.password), True)

    def test_get_name_by_id(self):
        pass
        # user = UserModel()
        # hashed_passwd = Utils.hash_password("huhu")
        # UserEntity(email="phuongvuong1998@gmail.com", password=hashed_passwd, active=0).save()
        # _user = UserEntity.objects(email__exact='phuongvuong1998@gmail.com')
        # print(_user)
        # self.assertTrue(str(len(_user)), "1")

    #     try:
    #         self.objects(email__exact=email).update(set__password=psw)
    #         return True, None
    #     except Exception as e:
    #         return False, e.__str__()

    # def test_delete(self):
    #     user = User(email="phuongvuong@gmail.com", password="huhu").save()
    #     user.delete()
    #     user.save()
    #     _user = User.objects(email__exact="phuongvuong@gmail.com")
    #     self.assertTrue(str(len(_user)), "0")
    #
    # def test_update(self):
    #     user = User(email="phuongvuong@gmail.com", password="huhu", active=0).save()
    #     user.active = 1
    #     user.save()
    #     self.assertTrue(user.active, 1)

    # def query_paginate(self, page):
    #     users = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
    #     return users.items, users.pages
    #
    # def update_basic(self, email, birthday=None, gender=None, favorite_categories=None):
    #     try:
    #         self.objects(email__exact=email).update(set__birthday=birthday)
    #         self.objects(email__exact=email).update(set__gender=gender)
    #         self.objects(email__exact=email).update(set__favorite_categories=favorite_categories)
    #         return True, None
    #     except Exception as e:
    #         return False, e.__str__()
    #
    # def update_psw(self, email, psw):
    #     try:
    #         self.objects(email__exact=email).update(set__password=psw)
    #         return True, None
    #     except Exception as e:
    #         return False, e.__str__()
    #
    # def update_link_image(self, email, link_image):
    #     try:
    #         self.objects(email__exact=email).update(set__link_image=link_image)
    #         # UserEntity.reindex()
    #         return True, None
    #     except Exception as e:
    #         return False, e.__str__()
    #
    # def turn_on_acc(self, email):
    #     try:
    #         self.objects(email__exact=email).update(set__active=1)
    #         # UserEntity.reindex()
    #         return True, None
    #     except Exception as e:
    #         return False, e.__str__()
    #
    # @classmethod
    # def create(cls, email, password, active):
    #     try:
    #         user = UserEntity(email=email, password=password, active=active).save()
    #         UserEntity.add_to_index_into_table(user)
    #         return True, None
    #     except Exception as e:
    #         return False, e.__str__()
    #
    # # def trigger_user_store_rel(self, uid):
    # #     stores = StoreEntity.objects
    # #     usrel = USRelEntity.objects
    # #     for store in stores:
    # #         classify = 1 + 2
    # #         usrel.create(uid, store.id, classify)
    #
    # def count(self):
    #     return self.objects.count()
    #
    # def query_recent(self):
    #     return self.objects.order_by("created_at")
    #
    # def changeStatus(self, id, active):
    #     try:
    #         self.objects(id__exact=id).update(set__active=active)
    #         return True, None
    #     except Exception as e:
    #         return False, e.__str__()
    #
    # def delete(self, user_id):
    #     try:
    #         user = UserEntity.objects(id=user_id).get()
    #         user.delete()
    #         user.save()
    #         return
    #     except Exception as e:
    #         return False, e.__str__()
    #
