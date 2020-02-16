from flask_mongoengine import Pagination
from app.entity.mongo.category import Category as CategoryEntity
from constants import Pages


class CategoryModel(CategoryEntity):
    objects = CategoryEntity.objects

    def query_paginate(self, page):
        categories = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return categories.items, categories.pages

    def find(self, name):
        return self.objects(name__exact=name)

    def find_by_id(self, category_id):
        return self.objects(id__exact=category_id)

    def query_by_brand_id(self, brand_id):
        return self.objects(brand_id__exact=brand_id)

    def edit(self, _id, name, brand_id):
        try:
            self.objects(id__exact=_id).update(set__name=name, set__brand_id=brand_id)
            CategoryEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()

    @classmethod
    def create(cls, name, brand_id):
        try:
            CategoryEntity(name=name, brand_id=brand_id).save()
            CategoryEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()
