from flask_mongoengine import Pagination
from app.entity.category import Category as CategoryEntity
from constants import Pages
from bson import ObjectId

class CategoryModel(CategoryEntity):
    objects = CategoryEntity.objects

    def get_name_by_id(self, category_id):
        return self.objects.get(id=category_id).name

    def get_name_link_by_id(self, category_id):
        return self.objects.get(id=category_id).name_link

    def query_all(self):
        return self.objects

    def query_paginate(self, page):
        categorys = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return categorys.items, categorys.pages

    def find_by_id(self, category_id):
        return self.objects(id__exact=category_id)
        
    def findAllById(self, listIds):
        categories =[]
        for x in listIds: 
            categories = categories + [self.objects(id__exact=x)]
        return categories

    def find_by_name(self, name):
        return self.objects(name__exact=name)
