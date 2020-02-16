from flask import Blueprint, render_template, current_app, request, jsonify, redirect, url_for, make_response

from app import cache
from app.CRUD.store.forms import StoreForm
from app.CRUD.address.models import AddressModel
from app.CRUD.store.models import StoreModel
from constants import Pages

store_blueprint = Blueprint(
    'store', __name__, template_folder='templates')


@store_blueprint.route('/api/list', methods=['GET'])
def list_store_api():
    store = StoreModel()
    address = AddressModel()
    page = request.args.get('page', 1, type=int)
    stores, total_pages = store.query_paginate(page)
    print(total_pages)
    data = []
    for store in stores:
        result, error = address.get_name_by_id(store.address_id)
        if error:
            return make_response(jsonify(error=error), 404)
        data.append({"id": str(store.id), 'address_name': result, "name": store.store_name})
    res = {
        "total_pages": total_pages,
        "data": data
    }

    return make_response(jsonify(res), 200)


@store_blueprint.route('/', methods=['GET'])
@cache.cached(timeout=5)
def list_store(error=None, form=None):
    address = AddressModel()
    if form is None:
        form = StoreForm()
    store = StoreModel()
    page = request.args.get('page', 1, type=int)
    stores, total_pages = store.query_paginate(page)
    addresses = address.query_all()
    return render_template('CRUD/store/list.html', total_pages=total_pages, addresses=addresses, store_active="active",
                           form=form, visible_page=Pages.VISIBLE_PAGE.value)


@store_blueprint.route('/create', methods=['GET', 'POST'])
def create_store(error=None):
    form = StoreForm()
    address = AddressModel()
    store = StoreModel()
    addresses = address.query_all()
    if form.validate_on_submit():
        if request.method == 'POST':
            store_name = request.form['store_name']
            address_id = request.form['address_id']
            store_exist = store.find(store_name)
            print("store_exist:", store_exist)
            if len(store_exist) == 0:
                return store.create(store_name, address_id) and redirect('/store')
            else:
                error = "Your store is error"
    return render_template('CRUD/store/create.html', addresses=addresses, error=error, store_active="active", form=form)


@store_blueprint.route('/', methods=['POST'])
def edit_store():
    form = StoreForm()
    store = StoreModel()
    if form.validate_on_submit():
        store_id = request.form['store_id']
        store_name = request.form['store_name']
        address_id = request.form['address_id']
        result, error = store.edit(store_id, store_name, address_id)
        if error:
            return list_store(error)
    return list_store(form=form)
