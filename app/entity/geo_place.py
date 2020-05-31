from mongoengine.document import Document
from mongoengine.fields import *
import datetime
from app.main.search.models import SearchableMixin


class GeoPlace(Document, SearchableMixin):
    __tablename__ = 'geo_place_mongo'
    __searchable__ = ['name']

    name = StringField(max_length=255, required=True)
    link_image = ListField()
    link_gg = StringField()
    link_foody = StringField()

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_on = DateTimeField(default=datetime.datetime.now)

    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<Geo Place %r>' % (self.name)
