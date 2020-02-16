from flask_mongoengine import Pagination
from app.entity.mongo.color import Color as ColorEntity
from constants import Pages


class ColorModel(ColorEntity):
    objects = ColorEntity.objects

    def get_value_by_id(self, color_id):
        return self.objects.get(id=color_id).value

    def query_all(self):
        return self.objects

    def query_paginate(self, page):
        colors = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return colors.items, colors.pages

    def find(self, value):
        return self.objects(value__exact=value)

    def edit(self, _id, value):
        try:
            self.objects(id__exact=_id).update(set__value=value)
            ColorEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()

    @classmethod
    def create(cls, value):
        try:
            ColorEntity(value=value).save()
            ColorEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()