import mongoengine
from app.main.search.models import SearchableMixin


class User(mongoengine.Document, SearchableMixin):
    __tablename__ = 'user_mongo'
    __searchable__ = ['user']

    email = mongoengine.StringField(max_length=255, required=True, unique=True)
    password = mongoengine.StringField(max_length=255)
    email_fb = mongoengine.StringField(max_length=255)
    id_fb = mongoengine.StringField(max_length=255)

    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<User %r>' % (self.email)
