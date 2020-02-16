from flask_mongoengine import Pagination
from app.entity.mongo.variant import ProductVariant as ProductVariantEntity
from constants import Pages


class ProductVariantModel(ProductVariantEntity):
    objects = ProductVariantEntity.objects

    def query_paginate(self, page):
        variants = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return variants.items, variants.pages, variants.page

    def query_all(self):
        return self.objects

    def query_by_id(self, _id):
        return self.objects(id__exact=_id)

    def edit(self, _id, price, product_id, store_id, color_id):
        try:
            self.objects(id__exact=_id).update(set__price=price, set__product_id=product_id, set__store_id=store_id,
                                               set__color_id=color_id)
            ProductVariantEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()

    @classmethod
    def create(cls, price, product_id, store_id, color_id):
        try:
            ProductVariantEntity(price=price, product_id=product_id, store_id=store_id, color_id=color_id).save()
            ProductVariantEntity.reindex()
            return True, None
        except Exception as e:
            return False, e.__str__()