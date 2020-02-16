from flask import Blueprint, render_template, request, make_response, jsonify, redirect

from app import cache
from app.CRUD.brand.forms import BrandForm
from app.CRUD.brand.models import BrandModel
from constants import Pages

brand_blueprint = Blueprint('brand', __name__, template_folder='templates')


@brand_blueprint.route('/api/list', methods=['GET'])
def list_brand_api():
    page = request.args.get('page', 1, type=int)
    brand = BrandModel()
    brands, total_pages = brand.query_paginate(page)
    res = {
        "total_pages": total_pages,
        "data": [{"id": str(brand.id), "name": brand.name} for brand in brands],
    }
    return make_response(jsonify(res), 200)


@brand_blueprint.route('/', methods=['GET'])
@cache.cached(timeout=5)
def list_brand(error=None, form=None):
    if form is None:
        form = BrandForm()
    page = request.args.get('page', 1, type=int)
    brand = BrandModel()
    brands, total_pages = brand.query_paginate(page)
    return render_template('CRUD/brand/list.html', total_pages=total_pages, brand_active="active", form=form, error=error, visible_page=Pages.VISIBLE_PAGE.value)


@brand_blueprint.route('/create', methods=['GET', 'POST'])
def create_brand(error=None):
    form = BrandForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            brand_name = request.form['brand_name']
            result, error = BrandModel.create(brand_name)
            if error:
                return list_brand(error)
            return redirect('/brand')
    return render_template('CRUD/brand/create.html', error=error, brand_active="active", form=form)


@brand_blueprint.route('/', methods=['POST'])
def edit_brand():
    form = BrandForm()
    brand = BrandModel()
    if form.validate_on_submit():
        brand_id = request.form['brand_id']
        brand_name = request.form['brand_name']
        result, error = brand.edit(brand_id, brand_name)
        if error:
            return list_brand(error)
    return list_brand(form=form)
