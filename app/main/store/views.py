from functools import wraps
import math
from flask import redirect, render_template, Blueprint, session, request

from app.main.store.forms import StoreForm
from app.main.store.models import StoreModel
from app.main.category.models import CategoryModel
from app.main.address.models import AddressModel
from app.main.auth.views import login_required

from utils import Utils
from constants import CLASS_LIST

store_blueprint = Blueprint(
    'store', __name__, template_folder='templates')


@store_blueprint.route("/stores/<string:store_id>", methods=["GET"])
def view_detail(store_id=None):
    # form = StoreForm()
    stores = StoreModel()
    categories = CategoryModel()
    store = stores.find_by_id(store_id)
    category = categories.findAllById(store[0].categories_id)
    address = AddressModel().find_by_id(store[0].address_id)
    classify = CLASS_LIST[store[0].classification]
    star_s1, star_s2, star_s3, star_s4, star_s5, avr_star, cnt = countStar(store)
    return render_template('detail.html', store=store[0], category=category, address=address[0],
                           star_s1=star_s1, star_s2=star_s2, star_s3=star_s3, star_s4=star_s4, star_s5=star_s5,
                           avr_star=avr_star, cnt=cnt, classify=classify)


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


@store_blueprint.route('/stores/', methods=['GET'])
@login_required
def stores():
    page = request.args.get('page', 1, type=int)
    class_filter = request.args.get('classification', '', type=str)
    level_filter = request.args.get('level', '', type=str)

    filter = {
        "classification": class_filter,
        "level": level_filter
    }
    
    # add param
    additional_params = ''
    for key, value in filter.items():
        if value != '':
            additional_params += '&' + key + '=' + value
    store_model = StoreModel()
    categories = CategoryModel()

    stores, pages = store_model.query_paginate_sort(page, filter)
    datas = []
    for store in stores:
        address = AddressModel().find_by_id(store.address_id)
        cates = categories.findAllById(store.categories_id)
        classify = CLASS_LIST[store.classification]
        datas += [{
            "store": store,
            "cates": cates,
            "address": address,
            "classify": classify
        }]

    # address = 
    return render_template("listing.html", datas=datas, pages=pages, 
                            current_page=page, additional_params=additional_params)

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
