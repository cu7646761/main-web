# import mongoengine
# import datetime
# from app.main.search.models import SearchableMixin


# class UserStoreRel(mongoengine.Document, SearchableMixin):
#     __tablename__ = 'user_store_rel_mongo'
#     user_id = mongoengine.ObjectIdField()
#     storer_id = mongoengine.ObjectIdField()
#     classification = mongoengine.IntField()

#     created_at = mongoengine.DateTimeField(default=datetime.datetime.now)
#     updated_on = mongoengine.DateTimeField(default=datetime.datetime.now)


    
#     meta = {'allow_inheritance': True}

#     def __repr__(self):
#         return '<User Store Rel %r>' % (self.user_id)

