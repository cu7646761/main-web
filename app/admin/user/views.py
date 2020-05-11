import json
import os
from datetime import datetime

import googlemaps
from flask import render_template, Blueprint, session, request, make_response, jsonify, Response
from vietnam_provinces.enums.districts import ProvinceEnum
from werkzeug.utils import secure_filename, redirect
from app.main.address.models import AddressModel
from app.main.auth.views import login_required
from app.main.category.models import CategoryModel
from app.main.comment.models import CommentModel
from app.main.auth.models import UserModel
from constants import UPLOAD_FOLDER, LINK_IMG
from app.image.image_preprocessing import resize

user_admin_blueprint = Blueprint(
    'user_admin', __name__, template_folder='templates')

@user_admin_blueprint.route('/admin/user-management', methods=['GET'])
@login_required
def user(form=None):
    user = UserModel()
    users, total_pages = user.query_paginate(1)
    return render_template("admin/user-management.html", user=session['cur_user'], form=form,
                           total_pages=total_pages)
