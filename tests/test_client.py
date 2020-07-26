import json
import os
import unittest
from mongoengine import disconnect
from app.entity.user import User
from app.entity.store import Store
from app.entity.category import Category
from app.entity.comment import Comment
from app.entity.address import Address
from app.model.address import AddressModel
from app.model.category import CategoryModel
from constants import LINK_IMG_AVATAR_DEF
from utils import Utils
from app import create_app
from app.model.auth import UserModel

disconnect()


class FlaskClientTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

        # clean db
        cls_entity = [User, Store, Category, Comment, Address]
        res = [e.drop_collection() for e in cls_entity]

        # init db
        # -----  init user
        hashed_passwd = Utils.hash_password("huhu")
        user = UserModel()
        user.create(email="phuongvuong1998@gmail.com", password=hashed_passwd, active=2)
        user.create(email="phuongvuong1@gmail.com", password=hashed_passwd, active=1)
        user.create(email="phuongvuong2@gmail.com", password=hashed_passwd, active=1)
        user.create(email="phuongvuong3@gmail.com", password=hashed_passwd, active=0)

        _user = user.find_by_email("phuongvuong1998@gmail.com")[0]

        # ------  init category
        data_category = []
        with open(os.path.abspath(os.path.dirname(__file__)) + '/data/category.json', encoding="utf8") as f:
            data_category.append(json.load(f))
        category_old_lst = data_category[0]
        for x in category_old_lst:
            Category(name=x['name'], name_link=x['name_link']).save()

        #init store
        cate = CategoryModel()
        _cate = cate.find_by_name("Buffet")
        addr = Address(detail="200 đường Hai Bà Trưng, Thành phố Quảng Ngãi, Tỉnh Quảng Ngãi",
                       district="",
                       latitude="15.1331244",
                       longtitude="108.7980412").save()
        Store(
            name="Cửa hàng 1",
            link_image=[LINK_IMG_AVATAR_DEF],
            description="<p>Test 1</p>",
            address_id=addr,
            categories_id=_cate
        ).save()

        # login account
        with self.client:
            with self.client.session_transaction() as session:
                session['cur_user'] = _user
                session['logged'] = True
                session['pos'] = {'lat': '10.8225398', 'lng': '106.6379724'}
            response = self.client.post('/login', data=dict(
                email="phuongvuong1998@gmail.com",
                passwpord=hashed_passwd
            ), follow_redirects=True)
        self.assertIn(response.status, '200 OK')

    def tearDown(self):
        self.app_context.pop()
        cls_entity = [User, Store, Category, Comment, Address]
        res = [e.drop_collection() for e in cls_entity]
