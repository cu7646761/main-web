from flask import Blueprint, render_template, redirect, request, jsonify, session

from app.main.auth.views import login_required
from app.model.address import AddressModel
from app.model.auth import UserModel
from app.main.search.forms import SearchForm
from app.main.search.search import FullTextSearch, SuggestionSearch
from app.model.store import StoreModel
from utils import Utils

search_blueprint = Blueprint('search', __name__, template_folder='templates')


@search_blueprint.route('/full-text', methods=['GET'])
@login_required
def full_text():
    form = SearchForm()
    if not form.validate() or not form.q.data:
        return redirect('/login')
    cls_model = [StoreModel]
    # reindex_all = [model.reindex() for model in cls_model]
    kind_search = FullTextSearch()
    search_model = [model.search(form.q.data, 1, 10, kind_search) for model in cls_model]
    search_obj = []
    for obj, total in search_model:
        if not isinstance(total, int):
            search_obj.extend(total)

    store = StoreModel()
    for obj in search_obj:
        try:
            _store = store.find_by_name(obj['_source']['name'])
            obj['thumbnail'] = _store.link_image[0]
            obj['address'] = _store.address_id.detail
        except:
            continue

    if session['logged'] == True:
        session['search'] += form.q.data + " , "
    return render_template('index.html', search_obj=search_obj, form=form, user=session['cur_user'])


@search_blueprint.route('/full-text-admin-store', methods=['GET'])
@login_required
def full_text_admin_store():
    form = SearchForm()
    store = StoreModel()
    address = AddressModel()
    if not form.validate() or not form.q.data:
        return redirect('/login')
    cls_model = [StoreModel]
    # reindex_all = [model.reindex() for model in cls_model]
    kind_search = FullTextSearch()
    search_model = [model.search(form.q.data, 1, 10, kind_search) for model in cls_model]
    search_obj = []
    for obj, total in search_model:
        if not isinstance(total, int):
            search_obj.extend(total)

    if session['logged'] == True:
        session['search'] += form.q.data + " , "
    list_store = []
    for each in search_obj:
        try:
            _store = store.find_by_id(each['_id'])[0]
        except:
            continue
        str_delete = None
        if _store.deleted_at is None:
            str_delete = 'Chưa xoá'
        else:
            str_delete = _store.deleted_at
        list_store.append({
            "_id": each['_id'],
            "name": _store.name,
            "stars": _store.stars,
            "address": _store.address_id.detail,
            "price": _store.min_price + "-" + _store.max_price,
            "created_at": _store.created_at,
            "deleted_at": str_delete
        })
    return render_template('admin/store.html', search_obj=list_store, form=form, user=session['cur_user'],
                           store_active="active", total_pages=None, count=10)


@search_blueprint.route('/suggestion-store', methods=['POST'])
@login_required
def suggestion_store():
    search_term = request.data.decode("utf-8").split("=")[1]
    cls_model = [StoreModel]
    kind_search = SuggestionSearch()
    search_model = [model.search(search_term, 1, 10, kind_search) for model in cls_model]
    search_obj = []
    for obj, total in search_model:
        if not isinstance(total, int):
            search_obj.extend(total)

    return jsonify({"data": search_obj})


@search_blueprint.route('/full-text-admin-user', methods=['GET'])
@login_required
def full_text_admin_user():
    form = SearchForm()
    user = UserModel()
    address = AddressModel()
    if not form.validate() or not form.q.data:
        return redirect('/login')
    cls_model = [UserModel]
    # reindex_all = [model.reindex() for model in cls_model]
    kind_search = FullTextSearch()
    search_model = [model.search(form.q.data, 1, 10, kind_search) for model in cls_model]
    search_obj = []

    for obj, total in search_model:
        if not isinstance(total, int):
            search_obj.extend(total)
    if session['logged'] == True:
        session['search'] += form.q.data + " , "
    list_user = []
    for each in search_obj:
        try:
            _user = user.find_by_id(each['_id'])[0]
        except:
            continue
        active = ""
        if _user.active == 0:
            active = "Chưa kích hoạt"
        else:
            active = "Đã kích hoạt"
        try:
            list_user.append({
                "_id": each['_id'],
                "email": _user.email,
                "address": address.find_by_id(_user.address_id)[0].detail,
                "created_at": _user.created_at,
                "active": active
            })
        except:
            list_user.append({
                "_id": each['_id'],
                "email": _user.email,
                "address": "Người dùng chưa cập nhật địa chỉ.",
                "created_at": _user.created_at,
                "active": active
            })

    users, total_pages = user.query_paginate(1)
    return render_template('admin/user-management.html', search_obj=list_user, form=form, user=session['cur_user'],
                           user_active="active", total_pages=total_pages, count=user.count())

    if session['logged'] == True:
        session['search'] += form.q.data + " , "

@search_blueprint.route('/suggestion-user', methods=['POST'])
@login_required
def suggestion_user():
    search_term = request.data.decode("utf-8").split("=")[1]
    cls_model = [UserModel]
    # reindex_all = [model.reindex() for model in cls_model]
    kind_search = SuggestionSearch()
    search_model = [model.search(search_term, 1, 10, kind_search) for model in cls_model]
    search_obj = []
    for obj, total in search_model:
        if not isinstance(total, int):
            search_obj.extend(total)
    return jsonify({"data": search_obj})
