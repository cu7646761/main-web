import time
import math
import requests
import math
import nltk,re
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from constants import Pages, CLASS_LIST
from flask import redirect, render_template, Blueprint, session, request, request, jsonify, make_response

from app.main.store.forms import StoreForm
from app.model.store import StoreModel
from app.main.comment.forms import AddCommentForm
from app.model.category import CategoryModel
from app.model.address import AddressModel
from app.main.auth.views import login_required

from utils import Utils
from constants import CLASS_LIST
from app.model.comment import CommentModel

from flask.helpers import url_for
from math import sqrt
from constants import API_KEY
from mongoengine.queryset.visitor import Q

store_blueprint = Blueprint(
    'store', __name__, template_folder='templates')


@store_blueprint.route("/stores/<string:store_id>", methods=["GET", "POST"])
@login_required
def view_detail(store_id=None, page=1, db=list(), form=None, error=None):
    print(session['pos'])
    if form is None:
        form = AddCommentForm()
    # form = StoreForm()
    CommentModel.update(store_id)
    stores = StoreModel()
    categories = CategoryModel()
    store = stores.find_by_id(store_id)
    session['search'] = store[0].name_translate
    category = store[0].categories_id
    address = store[0].address_id
    star_s1, star_s2, star_s3, star_s4, star_s5, avr_star, cnt = countStar(store)
    current_user = None
    userAddress = None
    error = None
    try:
        if session['logged'] == True:
            current_user = session['cur_user']
            if current_user.address_id:
                userAddress = current_user.address_id
            
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
    # for comment in comments:e 'stores' referenced before
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
            if not star:
                error = "Star is required"
                return render_template('detail.html', store=store[0], category=category, address=address,
                                           star_s1=star_s1, star_s2=star_s2, star_s3=star_s3, star_s4=star_s4,
                                           star_s5=star_s5, avr_star=avr_star, cnt=cnt, store_id=store_id,
                                           current_user=current_user, form=form, error=error, user=current_user,
                                           entity_dict=entity_dict[0:15], API_KEY=API_KEY, cate_dict=type_sorted)
            if error is None:

                if current_user:
                    new_comment, error = CommentModel.create(store_id, comment, star, current_user.id)
                    
                else:
                    new_comment, error = CommentModel.create(store_id, comment, star, None)
                if error:
                    return render_template('detail.html', store=store[0], category=category, address=address,
                                           star_s1=star_s1, star_s2=star_s2, star_s3=star_s3, star_s4=star_s4,
                                           star_s5=star_s5, avr_star=avr_star, cnt=cnt, store_id=store_id,
                                           current_user=current_user, form=form, error=error, user=current_user,
                                           entity_dict=entity_dict[0:15], API_KEY=API_KEY, cate_dict=type_sorted)
                if comment !="":
                    text_tsl = Utils.sample_translate_text(comment, "en-US", "britcat3")
                    text = text_tsl.translations[0].translated_text.lower()
                    sentences = text.split(".")
                    score_list = []
                    et_dict = dict(store[0].entity_score)
                    for sentence in sentences:
                        if sentence == "":
                            continue
                        sc = Utils.predict_sentiment_online(sentence)
                        cleaned = re.sub(r"[^(a-zA-Z')\s]",'', sentence)
                        tokenize = word_tokenize(cleaned)
                        pos = nltk.pos_tag(tokenize)
                        allow_type = ["N"]
                        all_words = []
                        for w in pos:
                            if w[1][0] in allow_type:
                                all_words.append(w[0])
                        
                        for word in all_words:
                            if word == "i":
                                continue
                            uword = word.upper()

                            if not et_dict.get(uword, False):
                                et_dict[uword] = {
                                    "quantity": 1,
                                    "sentiment": sc
                                }
                            else:
                                et_dict[uword] = {
                                    "quantity": et_dict[uword]["quantity"]+1,
                                    "sentiment": et_dict[uword]["sentiment"]+sc               
                                }
                        score_list.append(sc)
                    score = sum(score_list)/len(score_list)
                    review_list = CommentModel().find_by_store_id(store_id)
                    quant_comment = review_list.filter(Q(detail__ne=None)&Q(detail__ne=""))
                    score_sentiment = (store[0].score_sentiment*(quant_comment.count()-1) + score)/quant_comment.count()
                    store[0].update(set__entity_score=et_dict, set__score_sentiment=score_sentiment)
                    # score = Utils.predict_sentiment_score(text)
                    # print(aka)
                # return redirect(request.url)

    return render_template('detail.html', store=store[0], category=category, address=address,
                           star_s1=star_s1, star_s2=star_s2, star_s3=star_s3, star_s4=star_s4, star_s5=star_s5,
                           avr_star=avr_star, cnt=cnt, store_id=store_id, current_user=current_user, form=form, error=error
                           , user=current_user, entity_dict=entity_dict[0:15], API_KEY=API_KEY, cate_dict=type_sorted)


@store_blueprint.route("/load-relative-store/<string:store_id>")
def load_relative_store(store_id):
    stores = StoreModel()
    categories = CategoryModel()
    store = stores.find_by_id(store_id)
    category = store[0].categories_id
    address = store[0].address_id
    # star_s1, star_s2, star_s3, star_s4, star_s5, avr_star, cnt = countStar(store)
    current_user = None
    userAddress = None
    try:
        if session['logged'] == True:
            current_user = session['cur_user']
            if current_user.address_id:
                userAddress = current_user.address_id
            
    except:
        pass

    if request.args:
        page = int(request.args.get("page"))
        recStore, pg = stores.find_optimize_by_categories(store[0].category_predict, store[0].categories_id, page, store[0].id)
        datas = []
        for rec in recStore:
            # classify = Utils.get_classification_by_score(rec.classification)
            # classCur =  Utils.get_classification_by_score(store[0].classification)
            # distance = "Không xác định"
            # disCur = "Không xác định"
            # x1 = float(rec.position.get("lat"))
            # y1 = float(rec.position.get("lng"))
            # xCur = float(store[0].position.get("lat"))
            # yCur = float(store[0].position.get("lng"))

            # if session["pos"] is not None:
            #     # x2 = float(session["pos"].get("lat"))
            #     # y2 = float(session["pos"].get("lng"))
            #     # distance = round(getDistanceFromLatLonInKm(x1,y1,x2,y2),1)
            #     # disCur = round(getDistanceFromLatLonInKm(xCur,yCur,x2,y2),1)
            # else:
            #     if session['logged'] == True:
            #         if current_user.address_id:
                        # x2 = float(userAddress.latitude)
                        # y2 = float(userAddress.longtitude)
                        # distance = round(getDistanceFromLatLonInKm(x1,y1,x2,y2),1)
                        # disCur = round(getDistanceFromLatLonInKm(xCur,yCur,x2,y2),1)
            # curStore ={
            #     # "classify":classCur,
            #     "distance":disCur,
            # }
            datas += [{
                "store": rec,
                # "classify": classify,
                # "distance": distance,
                # "curStore" :curStore,
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
                userAddress = AddressModel().find_by_id(current_user.address_id.id)
    except:
        pass

    store_model = StoreModel()
    store_cur = store_model.find_by_id(store_id_cur)[0]
    store_target = store_model.find_by_id(store_id_target)[0]
    # classCur =  Utils.get_classification_by_score(store_cur.classification)
    class_cur = store_cur.score_sentiment
    # classify_tar = Utils.get_classification_by_score(store_target.classification)
    classify_tar = store_target.score_sentiment
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
        "class_cur":round(class_cur,2),
        "dis_cur":disCur,
        "star_cur":store_cur.stars,
        "review_cur":store_cur.reviewer_quant,
        "name_cur": store_cur.name,
        "class_tar":round(classify_tar,2),
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
        comment_list = CommentModel().find_by_store_id(store[0].id)
        if counter == 0:
            cmt_list = comment_list[0: int(Pages['NUMBER_PER_PAGE'])]
            # db = CommentModel().findAllById(cmt_list)
            print(f"Returning posts 0 to {int(Pages['NUMBER_PER_PAGE'])}")
            # Slice 0 -> quantity from the db
            # res = make_response(jsonify(db), 200)

        elif counter == len(comment_list):
            print("No more posts")
            cmt_list = {}
            # res = make_response(jsonify({}), 200)

        else:
            cmt_list = comment_list[counter : counter + int(Pages['NUMBER_PER_PAGE'])]
            # db = CommentModel().findAllById(cmt_list)
            print(f"Returning posts {counter} to {counter + int(Pages['NUMBER_PER_PAGE'])}")
            # Slice counter -> quantity from the db
            # res = make_response(jsonify(db), 200)

        res = make_response(jsonify(cmt_list), 200)
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
        return 0, 0, 0, 0, 0, 0, 0

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

@store_blueprint.route('/stores/', methods=['GET', 'POST'])
@login_required
def stores():
    page = request.args.get('page', 1, type=int)
    class_filter = request.args.get('classification', '', type=str)
    level_filter = request.args.get('level', '', type=str)
    categories_filter = request.args.get('categories', '', type=str)
    cate_predict_filter = request.args.get('cate_predict', '', type=str)
    star_filter = request.args.get('star', '', type=str)
    quality_filter = request.args.get('quality', '', type=str)
    distance_filter = request.args.get('quality', '', type=str)

    if request.method == 'POST':
        categories_filter = ""
        cate_param = request.form.getlist("cate")
        for c in cate_param:
            categories_filter +=c+","
        categories_filter = categories_filter[:-1]
        star = request.form.get("star")
        star_filter = star
        quality = request.form.get("quality")
        quality_filter = quality
        level = request.form.get("level")
        level_filter = level
        distance = request.form.get("distance")
        distance_filter = distance


    filter = {
        "classification": class_filter,
        "level": level_filter,
        "categories": categories_filter,
        "cate_predict": cate_predict_filter,
        "star": star_filter,
        "quality": quality_filter,
        "distance": distance_filter
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

    stores, pages, num = store_model.query_paginate_sort(page, filter)
    datas = []
    for store in stores:
        address = store.address_id
        cates = store.categories_id
        # classify = CLASS_LIST[store.classification]
        # classify = Utils.get_classification_by_score(store.classification)
        datas += [{
            "store": store,
            "cates": cates,
            "address": address,
            # "classify": classify,
            "score": store.score_sentiment
        }]

    all_cates = categories.query_all()
    selected_cates = categories_filter.split(',')
    selected_dics = {
        "cates": {},
        "level": level_filter,
        "address": {},
        "star": star_filter,
        "quality": quality_filter,
        "distance": distance_filter
    }
    for cate in all_cates:
        selected_dics["cates"][cate.name_link] = False
        if cate.name_link in selected_cates:
            selected_dics["cates"][cate.name_link] = True
    return render_template("listing.html", datas=datas, pages=pages, num=num,
                           current_page=page, additional_params=additional_params,
                           categories=all_cates, selected_dics=selected_dics, user=session['cur_user'])

@store_blueprint.route("/store", methods=["POST"])
def get_store_api():
    store = StoreModel()
    try:
        name = request.form.get("name")
        return redirect('/stores/' + str(store.find_by_name(name).id))
    except:
        name = request.data.decode("utf-8").split("=")[1]
    return jsonify({"id": str(store.find_by_name(name).id)})