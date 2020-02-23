import mongoengine
import datetime
from app.main.search.models import SearchableMixin


class User(mongoengine.Document, SearchableMixin):
    __tablename__ = 'user_mongo'
    __searchable__ = ['auth']

    email = mongoengine.StringField(max_length=255, required=True, unique=True)
    password = mongoengine.StringField(max_length=255)
    email_fb = mongoengine.StringField(max_length=255)
    id_fb = mongoengine.StringField(max_length=255)
    birthday = mongoengine.DateTimeField()
    permission = mongoengine.IntField()
    favorite_categories = mongoengine.ListField()
    favorite_stores = mongoengine.ListField()
    gender = mongoengine.IntField()
    comments_list = mongoengine.ListField()

    created_at = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated_on = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<User %r>' % (self.email)
