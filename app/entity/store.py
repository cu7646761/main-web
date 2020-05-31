import datetime
from mongoengine.document import Document
from mongoengine.fields import *

from app.entity.address import Address
from app.entity.category import Category
from app.main.search.models import SearchableMixin


class Store(Document, SearchableMixin):
    __tablename__ = 'store_mongo'
    __searchable__ = ['name']
    meta = {
        'indexes': [
            {
                'fields': ['+classification']
            }],
        'allow_inheritance': True
    }
    name = StringField(max_length=255, required=True)
    name_translate = StringField(max_length=255)

    address_id = ReferenceField(Address)
    categories_id = ListField(ReferenceField(Category))

    min_price = StringField(default="")
    max_price = StringField(default="")
    link_image = ListField(default=[])

    stars = FloatField(default=0)
    link_gg = StringField(default=None)
    link_foody = StringField(default=None)

    star_s1 = IntField(default=0)
    star_s2 = IntField(default=0)
    star_s3 = IntField(default=0)
    star_s4 = IntField(default=0)
    star_s5 = IntField(default=0)
    description = StringField(max_length=500, default=None)

    name_translate = StringField(default="")
    type_store = DictField(default={})

    classification = FloatField(default=None)
    score_sentiment = FloatField(default=0)
    reviewer_quant = IntField(default=0)
    fixed = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_on = DateTimeField(default=datetime.datetime.now)
    deleted_at = DateTimeField(default=None)

    entity_score = DictField(default={})
    # entity_sentiment = DictField()
    position = DictField(default={})
    category_predict = StringField()

    def __repr__(self):
        return '<Store %r>' % (self.name)
