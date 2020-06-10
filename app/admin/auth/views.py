from flask import render_template, Blueprint, session, redirect
from functools import wraps
from app.model.auth import UserModel
from app.model.comment import CommentModel
from app.model.store import StoreModel
from constants import LINK_IMG_AVATAR_DEF

auth_admin_blueprint = Blueprint(
    'auth_admin', __name__, template_folder='templates')


def login_required_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            if session['logged'] and session['cur_user'].active == 1:
                return redirect("/")
            # if user is not logged in, redirect to login page
            if not session['logged'] or session['cur_user'].active != 2:
                return redirect("/login")
        except:
            return redirect("/login")
        return f(*args, **kwargs)

    return wrap


@auth_admin_blueprint.route('/', methods=['GET'])
@login_required_admin
def home(form=None):
    stores = StoreModel()
    users = UserModel()
    cmts = CommentModel()

    item, page = cmts.query_paginate_sort(1)
    recent_cmts = item[0:5]

    recent_cmts_detail = []
    for cmt in recent_cmts:
        user_name = 'Ẩn danh'
        # try:
        #     user = users.find_by_id(cmt.user_id)[0]
        #     email = user.email
        #     user_name = email[:email.find('@')]
        #     user_link = user.link_image
        # except:
        #     user_link = LINK_IMG_AVATAR_DEF
        # recent_cmts_detail.append(
        #     {
        #         'detail': cmt.detail,
        #         'store_name': stores.find_by_id(cmt.store_id)[0].name,
        #         'user_name': user_name,
        #         'user_link': user_link
        #     }
        # )
        try:
            # user = users.find_by_id(cmt.user_id)[0]
            email = cmt.user_id
            user_name = email[:email.find('@')]
            user_link = cmt.user_id.link_image
        except:
            user_link = LINK_IMG_AVATAR_DEF
        recent_cmts_detail.append(
            {
                'detail': cmt.detail,
                'store_name': cmt.store_id.name,
                'user_name': user_name,
                'user_link': user_link
            }
        )

    recent_store = stores.query_recent()[0:5]
    recent_store_detail = []
    for store in recent_store:
        recent_store_detail.append(
            {
                'link': store.link_image,
                'name': store.name
            }
        )

    return render_template("admin/index.html", user=session['cur_user'], form=form, count_stores=stores.count(),
                           count_users=users.count(), count_cmts=cmts.count(), recent_cmts_detail=recent_cmts_detail,
                           recent_store_detail=recent_store_detail, home_active="active")
