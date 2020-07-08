import json
from bs4 import BeautifulSoup
import re
from datetime import datetime
import googlemaps
from flask import render_template, Blueprint, session, request, make_response, jsonify, Response
from vietnam_provinces.enums.districts import ProvinceEnum
from werkzeug.utils import redirect

from app.admin.auth.views import login_required_admin
from app.admin.user.views import allowed_file
from app.image.image_storage import get_size, upload_image_gc, delete_image_gc
from app.model.address import AddressModel
from app.model.category import CategoryModel
from app.main.search.forms import SearchForm
from app.model.store import StoreModel
from constants import API_KEY
from utils import Utils

gmaps = googlemaps.Client(key=API_KEY)

store_admin_blueprint = Blueprint(
    'store_admin', __name__, template_folder='templates')


@store_admin_blueprint.route("/images/", methods=["POST"])
@login_required_admin
def upload_image_admin():
    file = request.files.get("image", "")

    if file.filename == '':
        return Response(json.dumps({"error": "No selected file"}), 400)
    elif not allowed_file(file.filename):
        return Response(json.dumps({"error": "Format of your file is png, jpg, jpeg"}), 400)

    date = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    name = file.filename.split('.')[0]
    ext = file.filename.split('.')[1]
    file.filename = name + "__" + date + "." + ext
    if int(get_size(file)) > 150000:
        return Response(json.dumps({"error": "Your image must be smaller than 150 KB"}), 400)

    link_file = upload_image_gc('bloganuong_images', image_file=file)

    if not link_file:
        return Response(json.dumps({"error": "Upload not success"}), 400)
    return Response(json.dumps({"image_url": link_file}), 200)


@store_admin_blueprint.route("/images/delete/", methods=["POST"])
@login_required_admin
def remove_image_admin():
    remove_img = request.form.get("delete_img", "")
    title = request.form.get("post-title", "")
    store = StoreModel()
    _store = store.find_by_name(title)
    _store.link_image.remove(remove_img)
    _store.save()
    filename = remove_img.replace("https://storage.googleapis.com/bloganuong_images/", "")
    res = delete_image_gc('bloganuong_images', filename)
    return Response(json.dumps({"status": "success"}), 200)


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
                           total_pages=total_pages, search_obj=[], count=store.count())


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
        min_price = post_data.get("min_price", "")
        max_price = post_data.get("max_price", "")

        st = store.find_lst_by_name(name)
        if len(st) != 0:
            return redirect('/admin/store/')

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
            "lat": latitude,
            "lng": longtitude
        }
        text_tsl = Utils.sample_translate_text(name, "en-US", "britcat3")
        des_tsl = Utils.sample_translate_text(description, "en-US", "britcat3")
        name_translate = text_tsl.translations[0].translated_text.lower()
        des_translate = des_tsl.translations[0].translated_text.lower()
        text_input = name_translate + " " + name_translate + " " + name_translate + " " + description + " "
        cate_predict_rs = Utils.predict_food_cate_online(text_input)
        category_predict = max(cate_predict_rs, key=cate_predict_rs.get)

        image_list.append(image)
        res, err = StoreModel.create(name, description, image_list, list_obj_cate, address_id, position, name_translate,
                                     category_predict, cate_predict_rs, min_price, max_price, float(latitude), float(longtitude))
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
        thumbnail = post_data.get("image", "")
        categories = post_data.get("categories", "")
        address_detail = post_data.get("address_detail", "")
        address_district = post_data.get("address_district", "")
        image_list = post_data.get("image_list", "")
        min_price = post_data.get("min_price", "")
        max_price = post_data.get("max_price", "")

        description_old = store_detail.description
        bs = BeautifulSoup(description_old, 'html.parser')
        images_old = bs.find_all('img', {'src': re.compile('.jpg')})
        arr_images_old = []
        for image in images_old:
            arr_images_old.append(image['src'])
        # if image_old not in image_new => delete old
        for img in arr_images_old:
            if img not in image_list:
                img_del = img.replace("https://storage.googleapis.com/bloganuong_images/", "")
                res = delete_image_gc('bloganuong_images', img_del)
        list_obj_cate = []
        for cate in categories:
            list_obj_cate.append(category.find_by_name(cate)[0])

        geocode_result = gmaps.geocode(address_detail)
        latitude = geocode_result[0].get('geometry').get('location').get('lat')
        longtitude = geocode_result[0].get('geometry').get('location').get('lng')
        position = {
            "lat": latitude,
            "lng": longtitude
        }

        res_address, err = AddressModel.update(store_detail.address_id.id, address_detail, address_district,
                                               str(latitude), str(longtitude))
        if err:
            return redirect('/admin/store/edit/' + store_id)
        image_list.append(thumbnail)
        res, err = StoreModel.update(name, description, image_list, list_obj_cate, store_id, res_address, min_price, max_price, position,
                                    float(latitude), float(longtitude))
        if err:
            return redirect('/admin/store/edit/' + store_id)
        return Response(json.dumps({"success": "yes"}), 200)
    return render_template("admin/edit-store.html", user=session['cur_user'], store_detail=store_detail,
                           address=store_detail.address_id.detail,
                           lst_cate_choose=[x.name for x in store_detail.categories_id], form=form,
                           store_active="active", min_price=store_detail.min_price, max_price=store_detail.max_price,
                           total_pages=total_pages, province_list=province_list, cate_list=category.query_all())


@store_admin_blueprint.route('/delete/<string:store_id>', methods=['GET'])
@login_required_admin
def delete_store(form=None, store_id=None):
    if store_id is not None:
        deleted_at = datetime.now()
        res, err = StoreModel.delete(store_id, deleted_at)
    return redirect('/admin/store/')
