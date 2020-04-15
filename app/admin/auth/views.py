from flask import render_template, Blueprint, session

from app.main.auth.models import UserModel
from app.main.auth.views import login_required
from app.main.comment.models import CommentModel
from app.main.store.models import StoreModel
from constants import LINK_IMG_AVATAR_DEF

auth_admin_blueprint = Blueprint(
    'auth_admin', __name__, template_folder='templates')


@auth_admin_blueprint.route('/', methods=['GET'])
@login_required
def home(form=None):
    stores = StoreModel()
    users = UserModel()
    cmts = CommentModel()

    item, page = cmts.query_paginate_sort(1)
    recent_cmts = item[0:5]

    recent_cmts_detail = []
    for cmt in recent_cmts:
        user_name = 'Ẩn danh'
        try:
            user = users.find_by_id(cmt.user_id)[0]
            email = user.email
            user_name = email[:email.find('@')]
            user_link = user.link_image
        except:
            user_link = LINK_IMG_AVATAR_DEF
        recent_cmts_detail.append(
            {
                'detail': cmt.detail,
                'store_name': stores.find_by_id(cmt.store_id)[0].name,
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
                           count_users=users.count(), count_cmts=cmts.count(), recent_cmts_detail=recent_cmts_detail,recent_store_detail=recent_store_detail)