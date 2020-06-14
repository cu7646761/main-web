from mongoengine.document import Document
from mongoengine.fields import *
import datetime

from app.entity.store import Store
from app.entity.user import User
from app.main.search.search import SearchableMixin


class Comment(Document, SearchableMixin):
    __tablename__ = 'comment'
    __searchable__ = ['detail']
    detail = StringField(max_length=1000)
    user_id = ObjectIdField(default=None)

    detail = StringField(max_length=1000, default=None)

    user_id = ReferenceField(User)
    store_id = ReferenceField(Store, required=True)

    comment_type = StringField(max_length=10)
    star_num = IntField()
    cus_name = StringField(max_length=255)
    sentiment_dict = DictField()

    created_at = DateTimeField(default=datetime.datetime.now())
    updated_on = DateTimeField(default=None)

    meta = {'allow_inheritance': True,
            'ordering': ['-updated_on']}

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_on = datetime.datetime.now()
        return super(Comment, self).save(*args, **kwargs)

    def __repr__(self):
        return '<Comment %r>' % (self.detail)