import datetime
import os
import json

from app.entity.address import Address
from app.entity.category import Category
from app.entity.store import Store
from app.entity.user import User
from app.entity.comment import Comment
from constants import LINK_IMG_AVATAR_DEF

MONGODB_DB = 'foodblog_opt1'
MONGODB_HOST = 'mongodb+srv://admin:britcat@clusteroptimize-wysnm.gcp.mongodb.net/foodblog_opt1?retryWrites=true&w=majority'

from mongoengine import *

connect(
    db=MONGODB_DB,
    host=MONGODB_HOST
)

# --------- Create store ----------
data_store = []
with open(os.path.abspath(os.path.dirname(__file__)) + '/db-backup-2/store.json', encoding="utf8") as f:
    data_store.append(json.load(f))
store_old_lst = data_store[0]

# data_address = []
# with open(os.path.abspath(os.path.dirname(__file__)) + '/db-backup-2/address.json', encoding="utf8") as f:
#     data_address.append(json.load(f))
# address_old_lst = data_address[0]

# data_category = []
# with open(os.path.abspath(os.path.dirname(__file__)) + '/db-backup-2/category.json', encoding="utf8") as f:
#     data_category.append(json.load(f))
# category_old_lst = data_category[0]
# for x in category_old_lst:
#     cate = Category(name=x['name'],name_link=x['name_link']).save()
#     print('ok')

data_user = []
with open(os.path.abspath(os.path.dirname(__file__)) + '/db-backup-2/user.json', encoding="utf8") as f:
    data_user.append(json.load(f))
user_old_lst = data_user[0]

data_comment = []
with open(os.path.abspath(os.path.dirname(__file__)) + '/db-backup-2/comment.json', encoding="utf8") as f:
    data_comment.append(json.load(f))
comment_old_lst = data_comment[0]

# ----------- Backup store
# test_1 = [store_old_lst[0]]
# for store_old in store_old_lst:
#
#     addr_old = None
#     for addr in address_old_lst:
#         if addr['_id'] == store_old['address_id']:
#             addr_old = addr
#             break
#
#     address = {
#         '_cls': 'Address',
#         'detail': addr_old['detail'],
#         'latitude': addr_old['latitude'],
#         'longtitude': addr_old['longtitude'],
#         'district': addr_old['district']
#     }
#
#     # address_new = Address(detail=addr_old['detail'], latitude=addr_old['latitude'], longtitude=addr_old['longtitude'], district=addr_old['district']).save()
#
#     categories_id_new = []
#     for cate in store_old['categories_id']:
#         cate_old = None
#         for x in category_old_lst:
#             if x['_id']['$oid'] == cate['$oid']:
#                 cate_old = x
#                 break
#         cate_new = Category.objects.get(name_link__exact=cate_old['name_link'])
#         categories_id_new.append(cate_new)
#
#     des = None
#     try:
#         des = store_old['description']
#         classification = store_old['classification']
#         cate_pre = store_old['category_predict']
#     except:
#         des = None
#         classification = 0
#         cate_pre = ""
# res_store = Store(
#     name=store_old['name'],
#     name_translate=store_old['name_translate'],
#     min_price=store_old['min_price'],
#     max_price=store_old['max_price'],
#     star_s1=store_old['star_s1'],
#     star_s2=store_old['star_s1'],
#     star_s3=store_old['star_s1'],
#     star_s4=store_old['star_s1'],
#     star_s5=store_old['star_s1'],
#     stars=store_old['stars'],
#     reviewer_quant=store_old['reviewer_quant'],
#     link_image=store_old['link_image'],
#     description=des,
#     type_store=store_old['type_store'],
#     classification=classification,
#     score_sentiment=store_old['score_sentiment'],
#     fixed=store_old['fixed'],
#     entity_score=store_old['entity_score'],
#     position=store_old['position'],
#     category_predict=cate_pre,
#     created_at=datetime.datetime.now(),
#     updated_on=None,
#     deleted_at=None,
#     address_id=address_new,
#     categories_id=categories_id_new
# ).save()
#
# print(res_store.name)

# ---------- Backup user
# test_2 = [user_old_lst[0]]
# for user_old in user_old_lst:
    # if user_old['email'] == 'andang12111998@gmail.com':
    # print(user_old)
    # email = StringField(max_length=255, required=True, unique=True)
    # password = StringField(max_length=255)
    # email_fb = StringField(max_length=255)
    # id_fb = StringField(max_length=255)
    # name = StringField(max_length=255)
    # birthday = DateTimeField()
    # permission = IntField()
    # infor_rec = StringField(default=" ")
    # gender = IntField()
    # active = IntField(default=0)
    # address_id = ReferenceField(Address)
    # favorite_categories = ListField(ReferenceField(Category))
    # favorite_stores = ListField(ReferenceField(Store))
    # link_image = StringField(default=LINK_IMG_AVATAR_DEF)
    # created_at = DateTimeField(default=datetime.datetime.now())
    # updated_on = DateTimeField(default=None)

    # cmt_new_lst = []
    # for cmt_user in user_old['comments_list']:
    #     cmt_old = None
    #     for cmt in comment_old_lst:
    #         if cmt['_id']['$oid'] == cmt_user['$oid']:
    #             cmt_old = cmt
    #             break
    #     if cmt_old is not None:
    #         # print(cmt_old)
    #         store_old_id = None
    #         for store in store_old_lst:
    #             if cmt_old['store_id'] == store['_id']:
    #                 store_old_id = store
    #         print(store)
    #         # cmt_new = Comment(detail=cmt_old['detail'],user_id=user_old,)
    #         cmt_new_lst.append(cmt_old)

    # try:
    #     addr_old = None
    #     for addr in address_old_lst:
    #         if addr['_id'] == user_old['address_id']:
    #             addr_old = addr
    #             break
    #     address_new = Address(detail=addr_old['detail'], latitude=addr_old['latitude'], longtitude=addr_old['longtitude'], district=addr_old['district']).save()
    #     # address_new = None
    # except:
    #     address_new = None
    #
    # try:
    #     user_new = User(
    #         email=user_old['email'],
    #         password=user_old['password'],
    #         email_fb=None,
    #         id_fb=None,
    #         name=user_old['name'],
    #         birthday=user_old['birthday'],
    #         infor_rec=user_old['infor_rec'],
    #         gender=0,
    #         active=2,
    #         address_id=address_new,
    #         favorite_categories=[],
    #         favorite_stores=[],
    #         link_image=user_old['link_image']
    #     ).save()
    # except:
    #     user_new = User(
    #         email=user_old['email'],
    #         password=user_old['password'],
    #         email_fb=None,
    #         id_fb=None,
    #         name=None,
    #         birthday=None,
    #         infor_rec=None,
    #         gender=0,
    #         active=2,
    #         address_id=address_new,
    #         favorite_categories=[],
    #         favorite_stores=[],
    #         link_image=LINK_IMG_AVATAR_DEF
    #     ).save()

# ---------- Backup comment
    # comment list #
    # detail = StringField(max_length=1000)
    # user_id = ReferenceField(User)
    # store_id = ReferenceField(Store)
    # comment_type = StringField(max_length=10)
    # star_num = IntField()
    # cus_name = StringField(max_length=255)
    # sentiment_dict = DictField()
    # created_at = DateTimeField(default=datetime.datetime.now())
    # updated_on = DateTimeField(default=None)

for user_old in user_old_lst:
    # for store in store_old_lst:
    if 'andang12111998@gmail.com' in user_old['email']:
        print(user_old['comments_list'])
        for cmt_old_id in user_old['comments_list']:
            for cmt_old in comment_old_lst:
                try:
                    if cmt_old['_id']['$oid'] == cmt_old_id['$oid']:
                        for store in store_old_lst:
                            if cmt_old['store_id'] == store['_id']:
                                if store['name'] != 'huhu':
                                    print(user_old)
                                    print(store)
                                    user_new = User.objects(email__exact=user_old['email'])[0]
                                    store_new = Store.objects(name__exact=store['name'])[0]

                                    cmt_new = Comment(detail=cmt_old['detail'],
                                                      user_id=user_new,
                                                      store_id=store_new,
                                                      star_num=cmt_old['star_num'],
                                                      cus_name="andang12111998").save()
                except:
                    continue


# for store in store_old_lst:
#     if store['name'] != 'huhu':
#         for cmt_old_id in store['comment_list']:
#             for cmt_old in comment_old_lst:
#                 if cmt_old['_id']['$oid'] == cmt_old_id['$oid']:
#                     print(store['name'])
#                     store_new = Store.objects(name__exact=store['name'])[0]
#                     try:
#                         sentiment_dict = cmt_old['sentiment_dict']
#                     except:
#                         # print(cmt_old['detail'])
#                         cmt_new = Comment(detail=cmt_old['detail'],
#                                           user_id=None,
#                                           store_id=store_new,
#                                           star_num=cmt_old['star_num'],
#                                           cus_name=cmt_old['cus_name'],
#                                           sentiment_dict={}).save()
#                         print('ok1')
#                         continue
#                     try:
#                         user_id = cmt_old['user_id']
#                     except:
#                         # print(cmt_old['detail'])
#                         cmt_new = Comment(detail=cmt_old['detail'],
#                                           user_id=None,
#                                           store_id=store_new,
#                                           star_num=cmt_old['star_num'],
#                                           cus_name=cmt_old['cus_name'],
#                                           sentiment_dict=cmt_old['sentiment_dict']).save()
#                         print('ok2')

# for i in range(len(comment_old_lst)):
#     if i > 615540:
#         print(i)
#         # print(comment_old_lst[i])
#         # print(comment_old_lst[i]['detail'])
#         # print(comment_old_lst[i]['cus_name'])
#         # # print(comment_old_lst[i]['user_id'])
#         # print(comment_old_lst[i]['star_num'])
#         # # print(comment_old_lst[i]['sentiment_dict'])
#         # cmt = Comment.objects(cus_name__exact=comment_old_lst[i]['cus_name'], star_num__exact=comment_old_lst[i]['star_num'])[0]
#         # print('-----------')
#         # print(cmt['detail'])
#         # print(cmt['cus_name'])
#         # print(cmt['star_num'])
#         # print(cmt['sentiment_dict'])
#         for store in store_old_lst:
#             if store['name'] != 'huhu' and comment_old_lst[i]['store_id'] == store['_id']:
#                 print(store['name'])
#                 store_new = Store.objects(name__exact=store['name'])[0]
#                 flat = 0
#                 try:
#                     cus_name = comment_old_lst[i]['cus_name']
#                 except:
#                     flat = 1
#                     cmt_new = Comment(detail=comment_old_lst[i]['detail'],
#                                       user_id=None,
#                                       store_id=store_new,
#                                       star_num=comment_old_lst[i]['star_num'],
#                                       cus_name=None,
#                                       sentiment_dict=comment_old_lst[i]['sentiment_dict']).save()
#                     print('ok0')
#                 if flat != 1:
#                     try:
#                         sentiment_dict = comment_old_lst[i]['sentiment_dict']
#                     except:
#                         flat = 1
#                         cmt_new = Comment(detail=comment_old_lst[i]['detail'],
#                                           user_id=None,
#                                           store_id=store_new,
#                                           star_num=comment_old_lst[i]['star_num'],
#                                           cus_name=comment_old_lst[i]['cus_name'],
#                                           sentiment_dict={}).save()
#                         print('ok1')
#                 if flat != 1:
#                     try:
#                         user_id = comment_old_lst[i]['user_id']
#                     except:
#                         cmt_new = Comment(detail=comment_old_lst[i]['detail'],
#                                           user_id=None,
#                                           store_id=store_new,
#                                           star_num=comment_old_lst[i]['star_num'],
#                                           cus_name=comment_old_lst[i]['cus_name'],
#                                           sentiment_dict=comment_old_lst[i]['sentiment_dict']).save()
#                         print('ok2')
#                 break
# {"user_id": ObjectId('5ebd08774828cb2789c1bfad')}

