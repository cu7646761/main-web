import os

import mongoengine
import datetime
from app.main.search.models import SearchableMixin
from constants import SERVER_NAME, LINK_IMG, LINK_IMG_AVATAR_DEF


class User(mongoengine.Document, SearchableMixin):
    __tablename__ = 'user_mongo'
    __searchable__ = ['email']

    email = mongoengine.StringField(max_length=255, required=True, unique=True)
    password = mongoengine.StringField(max_length=255)
    email_fb = mongoengine.StringField(max_length=255)
    id_fb = mongoengine.StringField(max_length=255)
    name = mongoengine.StringField(max_length=255)
    birthday = mongoengine.DateTimeField()
    permission = mongoengine.IntField()
    favorite_categories = mongoengine.ListField()
    favorite_stores = mongoengine.ListField()
    infor_rec = mongoengine.StringField(default="a ")

    # nam:0, nu:1, khac:2
    gender = mongoengine.IntField()
    comments_list = mongoengine.ListField()
    address_id = mongoengine.ObjectIdField()
    active = mongoengine.IntField(default=0)
    address_id = mongoengine.ObjectIdField()

    # save avatar
    link_image = mongoengine.StringField(default=LINK_IMG_AVATAR_DEF)

    created_at = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated_on = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<User %r>' % (self.email)
