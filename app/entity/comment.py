import mongoengine
import datetime
from app.main.search.models import SearchableMixin


class Comment(mongoengine.Document, SearchableMixin):
    __tablename__ = 'comment_mongo'
    __searchable__ = ['detail']
    detail = mongoengine.StringField(max_length=1000)
    user_id = mongoengine.ObjectIdField()
    store_id = mongoengine.ObjectIdField()
    # comment_type: s,a,b,c,d,e,f,g,h,i
    comment_type = mongoengine.StringField(max_length=10)
    star_num = mongoengine.IntField()
    cus_name = mongoengine.StringField(max_length=255)

    created_at = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated_on = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {'allow_inheritance': True,
            'ordering': ['-updated_on']}

    def __repr__(self):
        return '<Comment %r>' % (self.detail)