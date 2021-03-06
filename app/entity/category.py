from mongoengine.document import Document
from mongoengine.fields import *

from app.main.search.search import SearchableMixin


class Category(Document, SearchableMixin):
    __tablename__ = 'category'
    __searchable__ = ['name']

    name = StringField()
    name_link = StringField(unique=True)

    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<Category %r>' % (self.name)
