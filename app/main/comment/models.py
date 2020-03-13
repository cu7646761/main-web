from flask_mongoengine import Pagination
from app.entity.comment import Comment as CommentEntity
from app.entity.user import User as UserEntity
from app.entity.store import Store as StoreEntity
from constants import Pages
from bson import ObjectId

class CommentModel(CommentEntity):
    objects = CommentEntity.objects

    def get_name_by_id(self, comment_id):
        return self.objects.get(id=comment_id).name

    def query_all(self):
        return self.objects

    def query_paginate(self, page):
        comments = Pagination(self.objects, int(page), int(Pages['NUMBER_PER_PAGE']))
        return comments.items, comments.pages
    def query_paginate_sort(self, page):
        comments_sorted = self.objects.order_by("-updated_on").all()
        comments = Pagination(comments_sorted, int(page), int(Pages['NUMBER_PER_PAGE']))
        return comments.items, comments.pages
    

    def find_by_id(self, comment_id):
        return self.objects(id__exact=comment_id)
        
    def findAllById(self, listIds):
        comments_sorted = self.objects.order_by("-star_num").all()
        comments =[]
        for x in listIds: 
            comments = comments + [comments_sorted(id=x)]
        return comments    
    @classmethod
    def create(cls, store_id, detail, star, user_id):
        try:
            comment = CommentEntity(store_id=store_id, detail=detail,star_num=star)
            comment.save()
            user = UserEntity.objects(id=user_id).get()
            user.comments_list.append(comment.id)
            user.save()
            store = StoreEntity.objects(id=store_id).get()
            store.comment_list.append(comment.id)
            store.reviewer_quant = store.reviewer_quant + 1
            if (int(star) == 1):
                store.star_s1 = store.star_s1 + 1
            elif (int(star) == 2): 
                store.star_s2 = store.star_s2 + 1
            elif(int(star) == 3): 
                store.star_s3 = store.star_s3 + 1
            elif(int(star) == 4): 
                store.star_s4 = store.star_s4 + 1
            elif (int(star) == 5):
                store.star_s5 = store.star_s5 + 1
            store.stars =  round(((store.star_s1 * 1 + store.star_s2 * 2 + store.star_s3 * 3 + store.star_s4 * 4 + store.star_s5 * 5) / store.reviewer_quant),1)
            store.save()
            return True, None
        except Exception as e:
            return False, e.__str__()