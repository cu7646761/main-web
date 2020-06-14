import json
import os
import datetime

import googlemaps
from flask import render_template, Blueprint, session, request, make_response, jsonify, Response
from vietnam_provinces.enums.districts import ProvinceEnum
from werkzeug.utils import secure_filename, redirect

from app.admin.auth.views import login_required_admin
from app.model.address import AddressModel
from app.model.category import CategoryModel
from app.main.search.forms import SearchForm
from app.model.store import StoreModel
from constants import UPLOAD_FOLDER, LINK_IMG
from constants import API_KEY
from google.cloud import translate
from utils import Utils

gmaps = googlemaps.Client(key=API_KEY)

store_admin_blueprint = Blueprint(
    'store_admin', __name__, template_folder='templates')


@store_admin_blueprint.route("/images/", methods=["POST"])
@login_required_admin
def resize_image():
    file = request.files.get("image", "")
    file.filename = datetime.datetime.now().strftime("%H:%M:%S.%f - %b %d %Y") + "-" + file.filename
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    link_image_new = LINK_IMG + filename

    if not link_image_new:
        return Response(json.dumps({"error": "Upload not success"}), 400)

    return Response(json.dumps({"image_url": link_image_new}), 200)


@store_admin_blueprint.route('/api/list', methods=['GET'])
@login_required_admin
def list_store_api():
    page = request.args.get('page', 1, type=int)
    store = StoreModel()
    stores, total_pages = store.query_paginate(page)
    data = []
    for store in stores:
        data.append({
            "store_id": str(store.id),
            "name": store.name,
            "description": store.description,
            "stars": store.stars,
            "address": store.address_id.detail,
            "price": store.min_price + "-" + store.max_price,
            "create_at": store.created_at
        })

    res = {
        "total_pages": total_pages,
        "data": data
    }
    return make_response(jsonify(res), 200)


@store_admin_blueprint.route('/', methods=['GET'])
@login_required_admin
def home_store(form=None):
    store = StoreModel()
    if form is None:
        form = SearchForm()
    stores, total_pages = store.query_paginate(1)
    return render_template("admin/store.html", user=session['cur_user'], form=form, store_active="active",
                           total_pages=total_pages - 2, search_obj=[], count=store.count())


@store_admin_blueprint.route('/add/', methods=['GET', 'POST'])
@login_required_admin
def _store(form=None):
    store = StoreModel()
    stores, total_pages = store.query_paginate(1)
    province_list = list(ProvinceEnum)
    category = CategoryModel()
    address = AddressModel()

    if request.method == 'POST':
        post_data = request.get_json()
        name = post_data.get("name", "")
        description = post_data.get("description", "")
        image = post_data.get("image", "")
        categories = post_data.get("categories", "")
        address_detail = post_data.get("address_detail", "")
        address_district = post_data.get("address_district", "")
        image_list = post_data.get("image_list", "")
        list_obj_cate = []
        for cate in categories:
            list_obj_cate.append(category.find_by_name(cate)[0].id)

        geocode_result = gmaps.geocode(address_detail)
        latitude = geocode_result[0].get('geometry').get('location').get('lat')
        longtitude = geocode_result[0].get('geometry').get('location').get('lng')

        address_id, err = address.create_store(address_detail, address_district, str(latitude), str(longtitude))
        if err:
            return redirect('/admin/store/add/')
        position = {
            "lat":latitude,
            "lng":longtitude
        }
        text_tsl = Utils.sample_translate_text(name, "en-US", "britcat3")
        des_tsl = Utils.sample_translate_text(description, "en-US","britcat3")
        name_translate = text_tsl.translations[0].translated_text.lower()
        des_translate = des_tsl.translations[0].translated_text.lower()
        text_input = name_translate + " " + name_translate + " " + name_translate + " " + description + " "
        cate_predict_rs = Utils.predict_food_cate(text_input) 
        category_predict = max(cate_predict_rs, key=cate_predict_rs.get)
        image_list.append(image)
        res, err = StoreModel.create(name, description, image_list, list_obj_cate, address_id, position, name_translate,
                                     category_predict, cate_predict_rs)

        if err:
            return redirect('/admin/store/add/')
        return Response(json.dumps({"success": "yes"}), 200)

    return render_template("admin/add-store.html", user=session['cur_user'], form=form, store_active="active",
                           total_pages=total_pages, province_list=province_list, cate_list=category.query_all())


@store_admin_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@login_required_admin
def edit__store(form=None, store_id=None):
    store = StoreModel()
    category = CategoryModel()
    store_detail = store.find_by_id(store_id)[0]
    stores, total_pages = store.query_paginate(1)
    province_list = list(ProvinceEnum)

    if request.method == 'POST':
        post_data = request.get_json()

        name = post_data.get("name", "")
        description = post_data.get("description", "")
        image = post_data.get("image", "")
        categories = post_data.get("categories", "")
        address_detail = post_data.get("address_detail", "")
        address_district = post_data.get("address_district", "")
        image_list = post_data.get("image_list", "")

        delete_img = post_data.get("delete_img", "")

        list_obj_cate = []
        for cate in categories:
            list_obj_cate.append(category.find_by_name(cate)[0].id)

        geocode_result = gmaps.geocode(address_detail)
        latitude = geocode_result[0].get('geometry').get('location').get('lat')
        longtitude = geocode_result[0].get('geometry').get('location').get('lng')

        res_address, err = AddressModel.update(store_detail.address_id, address_detail, address_district,
                                               str(latitude), str(longtitude))
        if err:
            return redirect('/admin/store/edit/' + store_id)

        image_list.append(image)
        if delete_img != "":
            image_list.remove(delete_img)

        res, err = StoreModel.update(name, description, image_list, list_obj_cate, store_id, res_address.id)
        if err:
            return redirect('/admin/store/edit/' + store_id)
        return Response(json.dumps({"success": "yes"}), 200)
    return render_template("admin/edit-store.html", user=session['cur_user'], store_detail=store_detail,
                           address=store_detail.address_id.detail,
                           lst_cate_choose=[x.name for x in store_detail.categories_id], form=form,
                           store_active="active",
                           total_pages=total_pages, province_list=province_list, cate_list=category.query_all())


@store_admin_blueprint.route('/delete/<string:store_id>', methods=['GET'])
@login_required_admin
def delete_store(form=None, store_id=None):
    if store_id is not None:
        deleted_at = datetime.datetime.now
        res, err = StoreModel.delete(store_id, deleted_at)
    return redirect('/admin/store/')
