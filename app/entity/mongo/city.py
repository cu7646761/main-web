import mongoengine

from app.main.search.models import SearchableMixin


class City(mongoengine.Document, SearchableMixin):
    __tablename__ = 'city_mongo'
    __searchable__ = ['name']
    name = mongoengine.StringField(max_length=60, required=True, unique=True)
    mysql_id = mongoengine.StringField(max_length=100)
    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<City %r>' % (self.name)
