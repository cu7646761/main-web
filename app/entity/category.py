import mongoengine

from app.main.search.models import SearchableMixin


class Category(mongoengine.Document, SearchableMixin):
    __tablename__ = 'category_mongo'
    __searchable__ = ['name']
    name = mongoengine.StringField()
    
    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<Category %r>' % (self.name)
