from mongoengine.document import Document
from mongoengine.fields import *

from app.main.search.search import SearchableMixin

class Address(Document, SearchableMixin):
    __tablename__ = 'address'
    __searchable__ = ['detail']

    detail = StringField(max_length=255, required=True)
    district = StringField()
    latitude = StringField()
    longtitude = StringField()
    store_id = ObjectIdField(default=None)
    is_store = BooleanField(default=None)
    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<Address %r>' % (self.detail)
