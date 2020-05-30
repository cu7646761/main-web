import json
import os
from datetime import datetime

import googlemaps
from flask import Flask, render_template, Blueprint, session, request, make_response, jsonify, Response
from vietnam_provinces.enums.districts import ProvinceEnum
from werkzeug.utils import secure_filename, redirect
from app.main.address.models import AddressModel
from app.main.auth.views import login_required
from app.main.category.models import CategoryModel
from app.main.comment.models import CommentModel
from app.main.auth.models import UserModel
from app.main.search.forms import SearchForm
from constants import UPLOAD_FOLDER, LINK_IMG
from app.image.image_preprocessing import resize
from constants import API_KEY
from app.main.address.models import AddressModel
from app.main.auth.models import UserModel
from app.main.auth.views import login_required
from werkzeug.utils import secure_filename
from app.main.category.models import CategoryModel
from app.main.user.forms import UpdatePswForm
from constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, LINK_IMG, LINK_IMG_AVATAR_DEF, SERVER_NAME, GENDER
from utils import Utils
from vietnam_provinces.enums.districts import ProvinceEnum, ProvinceDEnum, DistrictEnum, DistrictDEnum
from constants import API_KEY

gmaps = googlemaps.Client(key=API_KEY)

user_admin_blueprint = Blueprint(
    'user_admin', __name__, template_folder='templates')


@user_admin_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def user(form=None):
    user = UserModel()
    count = user.count()
    if form is None:
        form = SearchForm()
    users, total_pages = user.query_paginate(1)
    return render_template("admin/user-management.html", user=session['cur_user'], form=form,
                           total_pages=total_pages, count=count, user_active="active", search_obj=[])


@user_admin_blueprint.route('/set-status/<string:user_id>/<int:status>', methods=['GET'])
@login_required
def getStatus(form=None, user_id=None, status=None):
    user = UserModel()
    user.changeStatus(user_id,status)
    return redirect("/admin/user-management")


@user_admin_blueprint.route('/api/list', methods=['GET'])
@login_required
def list_user_api():
    page = request.args.get('page', 1, type=int)
    user = UserModel()
    users, total_pages = user.query_paginate(page)
    address = AddressModel()
    data = []
    for user in users:
        if user.active != 2:
            active = ""
            userAddress = "Người dùng chưa cập nhật địa chỉ."
            if user.address_id is not None:
                userAddress = address.find_by_id(user.address_id)[0].detail
            if user.active == 1:
                active = "Đã kích hoạt"
            if user.active == 0:
                active = "Chưa kích hoạt"
            data.append({
                "user_id": str(user.id),
                "email": user.email,
                "address": userAddress,
                "active": active,
                "create_at": user.created_at
            })

    res = {
        "total_pages": total_pages,
        "data": data
    }
    return make_response(jsonify(res), 200)


@user_admin_blueprint.route('/delete/<string:user_id>', methods=['GET'])
@login_required
def delete_user(form=None, user_id=None):
    user = UserModel()
    if user_id is not None:
        user.delete(user_id)
    return redirect('/admin/user-management')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user_admin_blueprint.route('/district', methods=['GET'])
def get_district_by_city():
    city_id = request.args.get('city_id')
    district_list = list(DistrictEnum)
    dis_with_city = []
    for dis in district_list:
        if int(dis.province_code) == int(city_id):
            dis_with_city.append(dis)
    if not city_id:
        return jsonify({})
    return jsonify({'district': dis_with_city})


@user_admin_blueprint.route('/edit/<string:user_id>', methods=['GET'])
@login_required
def edit(error=None, form=None, user_id=None, success=None):
    user = UserModel().find_by_id(user_id)[0]
    print(user)
    print(user_id)
    print("gi")
    province_list = list(ProvinceEnum)
    cate = CategoryModel()
    if form is None:
        form = UpdatePswForm()

    address = AddressModel()
    addr = ""
    if user.address_id is None:
        addr = ""
    else:
        addr = address.find_by_id(user.address_id)[0].detail

    category = CategoryModel()
    lst_cate_choose = [category.find_by_id(x)[0].name for x in user.favorite_categories]

    return render_template("admin/edit-user.html",user=session['cur_user'], cur_user = user,  error=error, form=form, success=success, province_list=province_list, cate_list=cate.query_all(), address=addr,
    lst_cate_choose=lst_cate_choose)

@user_admin_blueprint.route('/edit/<string:user_id>/update-basic', methods=['POST'])
def update_basic(error=None, form=None, user_id =None):
    current_user =UserModel().find_by_id(user_id)[0]
    print(current_user)
    if form is None:
        form = UpdatePswForm()

    birthday = request.form.get("birthday")
    gender = request.form.get("gender")
    res_address = request.form.get("result-address")
    love_cate = request.form.getlist("love_cate")
    print(love_cate)
    print("check love")
    district = res_address.split(',')[1]
    geocode_result = gmaps.geocode(res_address)
    latitude = str(geocode_result[0].get('geometry').get('location').get('lat'))
    longtitude = str(geocode_result[0].get('geometry').get('location').get('lng'))
    address = AddressModel()

    if current_user.address_id:
        res, err = address.update(current_user.address_id, res_address, district, latitude, longtitude)
    else:
        res, err = address.create(current_user.id, res_address, district, latitude, longtitude)
    if err:
        return edit(error=err, user_id = user_id)

    list_obj_cate = []
    if love_cate == "":
        list_obj_cate = current_user.favorite_categories
    else:
        category = CategoryModel()
        if isinstance(love_cate, str):
            list_obj_cate.append(category.find_by_name(love_cate)[0].id)
        else:
            for cate in love_cate:
                list_obj_cate.append(category.find_by_name(cate)[0].id)

    email = current_user.email
    if gender == 'Nam':
        gender = 0
    elif gender == 'Nữ':
        gender = 1
    else:
        gender = 2
    result, err = UserModel().update_basic(email, birthday, gender, list_obj_cate)
    if err:
        return edit(error=err, user_id = user_id )
    return edit(success="Cập nhật thông tin người dùng thành công!", user_id = user_id)

