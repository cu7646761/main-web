from mongoengine.document import Document
from mongoengine.fields import *
import datetime

from app.entity.store import Store
from app.entity.user import User
from app.main.search.models import SearchableMixin


class Comment(Document, SearchableMixin):
    __tablename__ = 'comment_mongo'
    __searchable__ = ['detail']

    detail = StringField(max_length=1000)

    user_id = ReferenceField(User, require=False)
    store_id = ReferenceField(Store)

    comment_type = StringField(max_length=10)
    star_num = IntField()
    cus_name = StringField(max_length=255)
    sentiment_dict = DictField()

    created_at = DateTimeField(default=datetime.datetime.now)
    updated_on = DateTimeField(default=datetime.datetime.now)

    meta = {'allow_inheritance': True,
            'ordering': ['-updated_on']}

    def __repr__(self):
        return '<Comment %r>' % (self.detail)