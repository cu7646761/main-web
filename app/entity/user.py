from mongoengine.document import Document
from mongoengine.fields import *
import datetime

from app.entity.address import Address
from app.entity.category import Category
from app.entity.store import Store
from app.main.search.search import SearchableMixin
from constants import SERVER_NAME, LINK_IMG, LINK_IMG_AVATAR_DEF


class User(Document, SearchableMixin):
    __tablename__ = 'user'
    __searchable__ = ['email']

    email = StringField(max_length=255, required=True, unique=True)
    password = StringField(max_length=255)
    email_fb = StringField(max_length=255, default="")
    id_fb = StringField(max_length=255, default="")
    name = StringField(max_length=255)
    birthday = DateTimeField()
    infor_rec = StringField(default=" ")

    # nam:0, nu:1, khac:2
    gender = IntField()
    active = IntField(default=0)

    comments_list = ListField()
    address_id = ReferenceField(Address)
    favorite_categories = ListField(ReferenceField(Category))
    favorite_stores = ListField(ReferenceField(Store))

    link_image = StringField(default=LINK_IMG_AVATAR_DEF)

    created_at = DateTimeField(default=datetime.datetime.now())
    updated_on = DateTimeField(default=None)

    meta = {'allow_inheritance': True}

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_on = datetime.datetime.now()
        return super(User, self).save(*args, **kwargs)

    def __repr__(self):
        return '<User %r>' % (self.email)
