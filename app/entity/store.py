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
    address_id = mongoengine.ObjectIdField()
    categories_id = mongoengine.ListField()
    min_price = mongoengine.StringField()
    max_price = mongoengine.StringField()
    link_image = mongoengine.ListField()

    stars = mongoengine.FloatField()
    link_gg = mongoengine.StringField()
    link_foody = mongoengine.StringField()

    star_s1 = mongoengine.IntField()
    star_s2 = mongoengine.IntField()
    star_s3 = mongoengine.IntField()
    star_s4 = mongoengine.IntField()
    star_s5 = mongoengine.IntField()
    description = mongoengine.StringField(max_length=500)

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
    comment_list = mongoengine.ListField()
    type_store =mongoengine.DictField()

    classification = mongoengine.FloatField()
    score_sentiment = mongoengine.FloatField()
    reviewer_quant = mongoengine.IntField()
    fixed = mongoengine.BooleanField()

    created_at = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated_on = mongoengine.DateTimeField(default=datetime.datetime.now)
    deleted_at = mongoengine.DateTimeField(default=None)

    entity_score = mongoengine.DictField()
    entity_sentiment = mongoengine.DictField()
    position = mongoengine.DictField()
    category_predict = mongoengine.StringField()
    meta = {'allow_inheritance': True}

    
def __repr__(self):
        return '<Store %r>' % (self.name)