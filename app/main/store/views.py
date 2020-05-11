from functools import wraps
import time
import math
import requests
import math
from constants import Pages, CLASS_LIST
from flask import redirect, render_template, Blueprint, session, request, request, jsonify, make_response

from app.main.store.forms import StoreForm
from app.main.store.models import StoreModel
from app.main.comment.forms import AddCommentForm
from app.main.category.models import CategoryModel
from app.main.address.models import AddressModel
from app.main.auth.views import login_required

from utils import Utils
from constants import CLASS_LIST
from app.main.comment.models import CommentModel

from flask.helpers import url_for
from math import sqrt
from constants import API_KEY

store_blueprint = Blueprint(
    'store', __name__, template_folder='templates')


@store_blueprint.route("/stores/<string:store_id>", methods=["GET", "POST"])
@login_required
def view_detail(store_id=None, page=1, db=list(), form=None, error=None):
    if form is None:
        form = AddCommentForm()
    # form = StoreForm()
    stores = StoreModel()
    categories = CategoryModel()
    store = stores.find_by_id(store_id)
    category = categories.findAllById(store[0].categories_id)
    address = AddressModel().find_by_id(store[0].address_id)
    star_s1, star_s2, star_s3, star_s4, star_s5, avr_star, cnt = countStar(store)
    current_user = None
    userAddress = None
    try:
        if session['logged'] == True:
            current_user = session['cur_user']
            if current_user.address_id:
                userAddress = AddressModel().find_by_id(current_user.address_id)
            
    except:
        pass

    entity_dict = store[0].entity_score
    entity_dict = sorted(entity_dict.items(), key=lambda x: x[1]["quantity"], reverse=True)

    type_filtered = {k: v for k, v in store[0].type_store.items() if v >= 0.1}
    type_sorted = {k: v for k, v in sorted(type_filtered.items(), key=lambda item: item[1], reverse=True)}
    print(type_sorted)
    # page = request.args.get('page', 1, type=int)
    # comments, pages = CommentModel().query_paginate_sort(page)
    # datas = []
    # for comment in comments:
    #     if (str(store_id) == str(comment.store_id)):
    #         datas += [{
    #             "detail": comment.detail,
    #             "star_num": comment.star_num,
    #         }]

    if request.method == 'POST':
        form = AddCommentForm()
        commentModel = CommentModel()
        if form.validate_on_submit():
            name = request.form.get("name", "")
            comment = request.form.get("comment", "")
            star = request.form.get("star", "")
            if not comment:
                error = "Star is required"
            if error is None:

                if current_user:
                    new_comment, error = CommentModel.create(store_id, comment, star, current_user.id)
                    
                else:
                    new_comment, error = CommentModel.create(store_id, comment, star, None)
                if error:
                    return render_template('detail.html', store=store[0], category=category, address=address[0],
                                           star_s1=star_s1, star_s2=star_s2, star_s3=star_s3, star_s4=star_s4,
                                           star_s5=star_s5, avr_star=avr_star, cnt=cnt, store_id=store_id,
                                           current_user=current_user, form=form, error=error, user=current_user)
                return redirect(request.url)

    return render_template('detail.html', store=store[0], category=category, address=address[0],
                           star_s1=star_s1, star_s2=star_s2, star_s3=star_s3, star_s4=star_s4, star_s5=star_s5,
                           avr_star=avr_star, cnt=cnt, store_id=store_id, current_user=current_user, form=form
                           , user=current_user, entity_dict=entity_dict[0:15], API_KEY=API_KEY, cate_dict = type_sorted)


@store_blueprint.route("/load-relative-store/<string:store_id>")
def load_relative_store(store_id):
    stores = StoreModel()
    categories = CategoryModel()
    store = stores.find_by_id(store_id)
    category = categories.findAllById(store[0].categories_id)
    address = AddressModel().find_by_id(store[0].address_id)
    # star_s1, star_s2, star_s3, star_s4, star_s5, avr_star, cnt = countStar(store)
    current_user = None
    userAddress = None
    try:
        if session['logged'] == True:
            current_user = session['cur_user']
            if current_user.address_id:
                userAddress = AddressModel().find_by_id(current_user.address_id)
            
    except:
        pass

    if request.args:
        page = int(request.args.get("page"))
        recStore, pg = stores.find_optimize_by_categories(store[0].category_predict, store[0].categories_id, page)
        datas = []
        for rec in recStore:
            classify = Utils.get_classification_by_score(rec.classification)
            classCur =  Utils.get_classification_by_score(store[0].classification)
            distance = "Không xác định"
            disCur = "Không xác định"
            x1 = float(rec.position.get("lat"))
            y1 = float(rec.position.get("lng"))
            xCur = float(store[0].position.get("lat"))
            yCur = float(store[0].position.get("lng"))

            if session["pos"] is not None:
                x2 = float(session["pos"].get("lat"))
                y2 = float(session["pos"].get("lng"))
                distance = round(getDistanceFromLatLonInKm(x1,y1,x2,y2),1)
                disCur = round(getDistanceFromLatLonInKm(xCur,yCur,x2,y2),1)
            else:
                if session['logged'] == True:
                    if current_user.address_id:
                        x2 = float(userAddress[0].latitude)
                        y2 = float(userAddress[0].longtitude)
                        distance = round(getDistanceFromLatLonInKm(x1,y1,x2,y2),1)
                        disCur = round(getDistanceFromLatLonInKm(xCur,yCur,x2,y2),1)
            curStore ={
                "classify":classCur,
                "distance":disCur,
            }
            datas += [{
                "store": rec,
                "classify": classify,
                "distance": distance,
                "curStore" :curStore,
            }]
        rs = {
            "datas": datas,
            "end": pg
        }
        res = make_response(jsonify(rs), 200)
        print(res)
        return res


@store_blueprint.route("/load-compare/<string:store_id_cur>/<string:store_id_target>")
def load_compare(store_id_cur, store_id_target):
    current_user = None
    userAddress = None
    try:
        if session['logged'] == True:
            current_user = session['cur_user']
            if current_user.address_id:
                userAddress = AddressModel().find_by_id(current_user.address_id)
    except:
        pass

    store_model = StoreModel()
    store_cur = store_model.find_by_id(store_id_cur)[0]
    store_target = store_model.find_by_id(store_id_target)[0]
    classCur =  Utils.get_classification_by_score(store_cur.classification)
    classify_tar = Utils.get_classification_by_score(store_target.classification)
    distance = "Không xác định"
    disCur = "Không xác định"
    x1 = float(store_target.position.get("lat"))
    y1 = float(store_target.position.get("lng"))
    xCur = float(store_cur.position.get("lat"))
    yCur = float(store_cur.position.get("lng"))

    if session["pos"] is not None:
        x2 = float(session["pos"].get("lat"))
        y2 = float(session["pos"].get("lng"))
        distance = round(getDistanceFromLatLonInKm(x1,y1,x2,y2),1)
        disCur = round(getDistanceFromLatLonInKm(xCur,yCur,x2,y2),1)
    else:
        if session['logged'] == True:
            if current_user.address_id:
                x2 = float(userAddress[0].latitude)
                y2 = float(userAddress[0].longtitude)
                distance = round(getDistanceFromLatLonInKm(x1,y1,x2,y2),1)
                disCur = round(getDistanceFromLatLonInKm(xCur,yCur,x2,y2),1)
    data = {
        "class_cur":classCur,
        "dis_cur":disCur,
        "star_cur":store_cur.stars,
        "review_cur":store_cur.reviewer_quant,
        "name_cur": store_cur.name,
        "class_tar":classify_tar,
        "dis_tar":distance,
        "star_tar":store_target.stars,
        "review_tar":store_target.reviewer_quant,
        "name_tar":store_target.name
    }
    res = make_response(jsonify(data), 200)
    return res


@store_blueprint.route("/load/<string:store_id>")
def load(store_id):
    """ Route to return the posts """
    stores = StoreModel()
    store = stores.find_by_id(store_id)

    time.sleep(0.5)  # Used to simulate delay
    if request.args:
        counter = int(request.args.get("c"))  # The 'counter' value sent in the QS
        if counter == 0:
            cmt_list = store[0].comment_list[0: int(Pages['NUMBER_PER_PAGE'])]
            db = CommentModel().findAllById(cmt_list)
            print(f"Returning posts 0 to {int(Pages['NUMBER_PER_PAGE'])}")
            # Slice 0 -> quantity from the db
            res = make_response(jsonify(db), 200)

        elif counter == len(store[0].comment_list):
            print("No more posts")
            res = make_response(jsonify({}), 200)

        else:
            cmt_list = store[0].comment_list[counter : counter + int(Pages['NUMBER_PER_PAGE'])]
            db = CommentModel().findAllById(cmt_list)
            print(f"Returning posts {counter} to {counter + int(Pages['NUMBER_PER_PAGE'])}")
            # Slice counter -> quantity from the db
            res = make_response(jsonify(db), 200)

    return res


def countStar(store):
    if (store[0].reviewer_quant != 0):
        star_s1 = round((store[0].star_s1 / store[0].reviewer_quant * 100), 2)
        star_s2 = round((store[0].star_s2 / store[0].reviewer_quant * 100), 2)
        star_s3 = round((store[0].star_s3 / store[0].reviewer_quant * 100), 2)
        star_s4 = round((store[0].star_s4 / store[0].reviewer_quant * 100), 2)
        star_s5 = round((store[0].star_s5 / store[0].reviewer_quant * 100), 2)
        avr_star = round(((store[0].star_s1 * 1 + store[0].star_s2 * 2 + store[0].star_s3 * 3 + store[0].star_s4 * 4 +
                           store[0].star_s5 * 5) / store[0].reviewer_quant), 1)
        cnt = math.floor(avr_star)

        return star_s1, star_s2, star_s3, star_s4, star_s5, avr_star, cnt
    else:
        return 0, 0, 0, 0, 0, 0

def getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = deg2rad(lat2-lat1)
    dLon = deg2rad(lon2-lon1); 
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1))*math.cos(deg2rad(lat2))*math.sin(dLon/2)*math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)); 
    d = R * c
    return d
def deg2rad(deg):
    return deg*(math.pi/180)

@store_blueprint.route('/stores/', methods=['GET'])
@login_required
def stores():
    page = request.args.get('page', 1, type=int)
    class_filter = request.args.get('classification', '', type=str)
    level_filter = request.args.get('level', '', type=str)
    categories_filter = request.args.get('categories', '', type=str)
    cate_predict_filter = request.args.get('cate_predict', '', type=str)
    filter = {
        "classification": class_filter,
        "level": level_filter,
        "categories": categories_filter,
        "cate_predict": cate_predict_filter
    }

    # add param
    additional_params = ''
    for key, value in filter.items():
        if value != '':
            additional_params += '&' + key + '=' + value
    store_model = StoreModel()
    categories = CategoryModel()
    comment_model = CommentModel()
    adr_model = AddressModel()

    stores, pages = store_model.query_paginate_sort(page, filter)
    datas = []
    for store in stores:
        address = AddressModel().find_by_id(store.address_id)
        cates = categories.findAllById(store.categories_id)
        # classify = CLASS_LIST[store.classification]
        classify = Utils.get_classification_by_score(store.classification)
        datas += [{
            "store": store,
            "cates": cates,
            "address": address,
            "classify": classify
        }]

    all_cates = categories.query_all()
    selected_cates = categories_filter.split(',')
    selected_dics = {
        "cates": {},
        "level": level_filter,
        "address": {}
    }
    for cate in all_cates:
        selected_dics["cates"][cate.name_link] = False
        if cate.name_link in selected_cates:
            selected_dics["cates"][cate.name_link] = True
    # address = 
    return render_template("listing.html", datas=datas, pages=pages,
                           current_page=page, additional_params=additional_params,
                           categories=all_cates, selected_dics=selected_dics, user=session['cur_user'])


# @auth_blueprint.route("/detail-store", methods=["POST"])
# def post_signup(error=None):
#     form = DetailStoreForm()
#     if form.validate_on_submit():
#         user = StoreModel()
#         email = request.form.get("email", "")
#         password = request.form.get("password", "")
#         if not email:
#             error = "Email is required"
#         elif not password:
#             error = "Password is required"
#         elif len(user.find_by_email(email)) == 1:
#             error = "Store {0} is already registered.".format(email)
#         if error is None:
#             # the name is available, store it in the database
#             hashed_passwd = Utils.hash_password(password)
#             new_user, error = StoreModel.create(email, hashed_passwd)
#             if error:
#                 return render_template('signup.html', error=error, success=None, form=form)
#             return render_template('signup.html', success="You have signed up successfully", form=form)
#     return render_template('signup.html', error=error, form=form)

@store_blueprint.route("/store", methods=["POST"])
def get_store_api():
    store = StoreModel()
    try:
        name = request.form.get("name")
        return redirect('/stores/' + str(store.find_by_name(name).id))
    except:
        name = request.data.decode("utf-8").split("=")[1]
    return jsonify({"id": str(store.find_by_name(name).id)})
    