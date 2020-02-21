import mongoengine
import datetime
from app.main.search.models import SearchableMixin


class Store(mongoengine.Document, SearchableMixin):
    __tablename__ = 'store_mongo'
    __searchable__ = ['store']

    name = mongoengine.StringField(max_length=255, required=True, unique=True)
    address_id = mongoengine.ObjectIdField()
    categories_id = mongoengine.ListField()
    min_price = mongoengine.LongField()
    max_price = mongoengine.LongField()
    link_image = mongoengine.StringField()
    link_gg = mongoengine.StringField()
    link_foody = mongoengine.StringField()
    star1s = mongoengine.IntField()
    star2s = mongoengine.IntField()
    star3s = mongoengine.IntField()
    star4s = mongoengine.IntField()
    star5s = mongoengine.IntField()
    description = mongoengine.StringField(max_length=500)
    comments = mongoengine.StringField(max_length=255)
    comments_a = mongoengine.IntField()
    comments_b = mongoengine.IntField()
    comments_c = mongoengine.IntField()
    comments_d = mongoengine.IntField()
    comments_e = mongoengine.IntField()
    comments_f = mongoengine.IntField()
    comments_g = mongoengine.IntField()
    comments_h = mongoengine.IntField()
    comments_i = mongoengine.IntField()
    comments_s = mongoengine.IntField()
    comments_list = mongoengine.ListField()
    classification = mongoengine.StringField(max_length=10)
    reviewer_quantity = mongoengine.IntField()

    created_at = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated_on = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {'allow_inheritance': True}

    
def __repr__(self):
        return '<Store %r>' % (self.name)