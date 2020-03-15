from app.entity.user_store_rel import as USRelEntity
from app.entity.user import as UserEntity
from app.entity.store import Store as StoreEntity
from constants import Pages
from bson import ObjectId
from constants import PRED_LIST, CLASS_LIST
from mongoengine.queryset.visitor import Q
from app.main.category.models import CategoryModel

class USRelModel(USRelEntity):
    objects = USRelEntity.objects

    def get_user_by_uid(self, uid):
        user = UserEntity.objects.get(id=uid)[0]
        return user

    def get_store_by_sid(self, sid):
        store = StoreEntity.objects.get(id=sid)[0]
        return store

    def query_all(self):
        return self.objects