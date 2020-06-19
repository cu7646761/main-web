import unittest
from mongoengine import disconnect
from app import create_app
from app.entity.user import User
from app.entity.store import Store
from app.entity.category import Category
from app.entity.comment import Comment
from app.entity.address import Address
from utils import Utils


class FlaskClientTestCase(unittest.TestCase):

    def setUp(self):
        disconnect()
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=False)

        # init db
        print("init")
        hashed_passwd = Utils.hash_password("huhu")
        user_1 = User(email="phuongvuong1998@gmail.com", password=hashed_passwd, active=0).save()

    def tearDown(self):
        self.app_context.pop()
        print("end")
        cls_entity = [User, Store, Category, Comment, Address]
        res = [e.drop_collection() for e in cls_entity]
