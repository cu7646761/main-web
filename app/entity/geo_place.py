import mongoengine
import datetime
from app.main.search.models import SearchableMixin


class GeoPlace(mongoengine.Document, SearchableMixin):
    __tablename__ = 'geo_place_mongo'
    __searchable__ = ['name']

    name = mongoengine.StringField(max_length=255, required=True)
    link_image = mongoengine.ListField()
    link_gg = mongoengine.StringField()
    link_foody = mongoengine.StringField()
    created_at = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated_on = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {'allow_inheritance': True}

    
def __repr__(self):
        return '<Geo Place %r>' % (self.name)