import json
import os
import datetime

import googlemaps
from flask import render_template, Blueprint, session, request, make_response, jsonify, Response
from vietnam_provinces.enums.districts import ProvinceEnum
from werkzeug.utils import secure_filename, redirect

from app.admin.auth.views import login_required_admin
from app.main.address.models import AddressModel
from app.main.auth.views import login_required
from app.main.category.models import CategoryModel
from app.main.comment.models import CommentModel
from app.main.store.models import StoreModel
from constants import UPLOAD_FOLDER, LINK_IMG
from app.image.image_preprocessing import resize

gmaps = googlemaps.Client(key='AIzaSyBFIs_p577J18Oqokx2EdZZVVk9XLLzk6Q')

store_admin_blueprint = Blueprint(
    'store_admin', __name__, template_folder='templates')


@store_admin_blueprint.route("/images/", methods=["POST"])
@login_required_admin
def resize_image():
    # base64_image = request.form.get("image_text", "")
    file = request.files.get("image", "")

    # file = resize(image_file)

    file.filename = datetime.now().strftime("%H:%M:%S.%f - %b %d %Y") + "-" + file.filename
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
    address = AddressModel()
    comment = CommentModel()
    data = []
    for store in stores:
        # data.append({
        #     "store_id": str(store.id),
        #     "name": store.name,
        #     "description": store.description,
        #     "stars": store.stars,
        #     "cmt_count": comment.find_by_store_id(store.id).count(),
        #     "address": address.find_by_id(store.address_id)[0].detail,
        #     "price": store.min_price + "-" + store.max_price,
        #     "create_at": store.created_at
        # })
        data.append({
            "store_id": str(store.id),
            "name": store.name,
            "description": store.description,
            "stars": store.stars,
            "address": address.find_by_id(store.address_id)[0].detail,
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
    stores, total_pages = store.query_paginate(1)
    return render_template("admin/store.html", user=session['cur_user'], form=form, store_active="active",
                           total_pages=total_pages - 2)


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

        address_id, err = address.create_store(address_detail, address_district, latitude, longtitude)
        if err:
            return redirect('/admin/store/add/')

        image_list.append(image)

        res, err = StoreModel.create(name, description, image_list, list_obj_cate, address_id)

        if err:
            return redirect('/admin/store/add/')
        return Response(json.dumps({"success": "yes"}), 200)

    return render_template("admin/add-store.html", user=session['cur_user'], form=form, store_active="active",
                           total_pages=total_pages, province_list=province_list, cate_list=category.query_all())


@store_admin_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@login_required_admin
def edit__store(form=None, store_id=None):
    store = StoreModel()
    store_detail = store.find_by_id(store_id)[0]

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

        delete_img = post_data.get("delete_img", "")

        list_obj_cate = []
        for cate in categories:
            list_obj_cate.append(category.find_by_name(cate)[0].id)

        geocode_result = gmaps.geocode(address_detail)
        latitude = geocode_result[0].get('geometry').get('location').get('lat')
        longtitude = geocode_result[0].get('geometry').get('location').get('lng')

        res_address, err = AddressModel.update(store_detail.address_id, address_detail, address_district, latitude,
                                               longtitude)

        if err:
            return redirect('/admin/store/edit/' + store_id)

        image_list.append(image)
        if delete_img != "":
            image_list.remove(delete_img)

        res, err = StoreModel.update(name, description, image_list, list_obj_cate, store_id, res_address.id)

        if err:
            return redirect('/admin/store/edit/' + store_id)
        return Response(json.dumps({"success": "yes"}), 200)

    address_obj = address.find_by_id(store_detail.address_id)[0]

    category = CategoryModel()
    lst_cate_choose = [category.find_by_id(x)[0].name for x in store_detail.categories_id]

    return render_template("admin/edit-store.html", user=session['cur_user'], store_detail=store_detail,
                           address=address_obj.detail, lst_cate_choose=lst_cate_choose, form=form,
                           store_active="active",
                           total_pages=total_pages, province_list=province_list, cate_list=category.query_all())


@store_admin_blueprint.route('/delete/<string:store_id>', methods=['GET'])
@login_required_admin
def delete_store(form=None, store_id=None):
    store = StoreModel()
    if store_id is not None:
        deleted_at = datetime.datetime.now
        res, err = StoreModel.delete(store_id, deleted_at)
    return redirect('/admin/store/')
