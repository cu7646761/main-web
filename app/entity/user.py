from mongoengine.document import Document
from mongoengine.fields import *
import datetime

from app.entity.address import Address
from app.entity.category import Category
from app.entity.comment import Comment
from app.entity.store import Store
from app.main.search.models import SearchableMixin
from constants import SERVER_NAME, LINK_IMG, LINK_IMG_AVATAR_DEF


class User(Document, SearchableMixin):
    __tablename__ = 'user_mongo'
    __searchable__ = ['email']

    email = StringField(max_length=255, required=True, unique=True)
    password = StringField(max_length=255)
    email_fb = StringField(max_length=255)
    id_fb = StringField(max_length=255)
    name = StringField(max_length=255)
    birthday = DateTimeField()
    permission = IntField()
    infor_rec = StringField(default=" ")

    # nam:0, nu:1, khac:2
    gender = IntField()
    active = IntField(default=0)

    comments_list = ListField(ReferenceField(Comment))
    address_id = ReferenceField(Address)
    favorite_categories = ListField(ReferenceField(Category))
    favorite_stores = ListField(ReferenceField(Store))

    link_image = StringField(default=LINK_IMG_AVATAR_DEF)

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_on = DateTimeField(default=datetime.datetime.now)

    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<User %r>' % (self.email)
