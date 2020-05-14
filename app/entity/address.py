import mongoengine

from app.main.search.models import SearchableMixin


class Address(mongoengine.Document, SearchableMixin):
    __tablename__ = 'address_mongo'
    __searchable__ = ['detail']
    detail = mongoengine.StringField(max_length=255, required=True)
    district = mongoengine.StringField()
    latitude = mongoengine.StringField()
    longtitude = mongoengine.StringField()
    
    meta = {'allow_inheritance': True}
    def __repr__(self):
        return '<Address %r>' % (self.detail)
