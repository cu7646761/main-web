import mongoengine
import datetime
from app.main.search.models import SearchableMixin


class Store(mongoengine.Document, SearchableMixin):
    __tablename__ = 'store_mongo'
    __searchable__ = ['name']
    meta = {        
        'indexes': [
            {
                'fields': ['+classification']	               
            }]
    }
    name = mongoengine.StringField(max_length=255, required=True)
    name_translate = mongoengine.StringField(max_length=255)
    address_id = mongoengine.ObjectIdField(required=True)
    categories_id = mongoengine.ListField(required=True)
    min_price = mongoengine.StringField(default="")
    max_price = mongoengine.StringField(default="")
    link_image = mongoengine.ListField(default=[])

    stars = mongoengine.FloatField(default=0)
    link_gg = mongoengine.StringField(default=None)
    link_foody = mongoengine.StringField(default=None)

    star_s1 = mongoengine.IntField(default=0)
    star_s2 = mongoengine.IntField(default=0)
    star_s3 = mongoengine.IntField(default=0)
    star_s4 = mongoengine.IntField(default=0)
    star_s5 = mongoengine.IntField(default=0)
    description = mongoengine.StringField(max_length=500, default=None)

    comments_a = mongoengine.IntField(default=None)
    comments_b = mongoengine.IntField(default=None)
    comments_c = mongoengine.IntField(default=None)
    comments_d = mongoengine.IntField(default=None)
    comments_e = mongoengine.IntField(default=None)
    comments_f = mongoengine.IntField(default=None)
    comments_g = mongoengine.IntField(default=None)
    comments_h = mongoengine.IntField(default=None)
    comments_i = mongoengine.IntField(default=None)
    comments_s = mongoengine.IntField(default=None)
    comment_list = mongoengine.ListField(default=[])
    name_translate = mongoengine.StringField(default="")
    type_store =mongoengine.DictField(default={})

    classification = mongoengine.FloatField(default=None)
    score_sentiment = mongoengine.FloatField(default=0)
    reviewer_quant = mongoengine.IntField(default=0)
    fixed = mongoengine.BooleanField(default=False)

    created_at = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated_on = mongoengine.DateTimeField(default=datetime.datetime.now)
    deleted_at = mongoengine.DateTimeField(default=None)

    entity_score = mongoengine.DictField(default={})
    # entity_sentiment = mongoengine.DictField()
    position = mongoengine.DictField(default={})
    category_predict = mongoengine.StringField()
    meta = {'allow_inheritance': True}

    
def __repr__(self):
        return '<Store %r>' % (self.name)