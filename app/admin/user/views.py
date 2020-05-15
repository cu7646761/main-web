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
    print("kaka")
    print(status)
    print(user_id)
    user.changeStatus(user_id, status)
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
