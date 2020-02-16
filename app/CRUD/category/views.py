from flask import Blueprint, render_template, current_app, request, jsonify, redirect, url_for, make_response

from app import cache
from app.CRUD.category.forms import CategoryForm
from app.CRUD.brand.models import BrandModel
from app.CRUD.category.models import CategoryModel
from constants import Pages

category_blueprint = Blueprint(
    'category', __name__, template_folder='templates')


@category_blueprint.route('/api/list', methods=['GET'])
def list_category_api():
    category = CategoryModel()
    brand = BrandModel()
    page = request.args.get('page', 1, type=int)
    categorys, total_pages = category.query_paginate(page)
    res = {
        "total_pages": total_pages,
        "data": [{"id": str(category.id), 'brand_name': brand.get_name_by_id(category.brand_id), "name": category.name} for
                 category in categorys],
    }
    return make_response(jsonify(res), 200)


@category_blueprint.route('/', methods=['GET'])
@cache.cached(timeout=5)
def list_category(error=None, form=None):
    brand = BrandModel()
    if form is None:
        form = CategoryForm()
    category = CategoryModel()
    page = request.args.get('page', 1, type=int)
    categorys, total_pages = category.query_paginate(page)
    brands = brand.query_all()
    return render_template('CRUD/category/list.html', total_pages=total_pages, brands=brands, category_active="active",
                           form=form, visible_page=Pages.VISIBLE_PAGE.value)


@category_blueprint.route('/create', methods=['GET', 'POST'])
def create_category(error=None):
    form = CategoryForm()
    brand = BrandModel()
    category = CategoryModel()
    brands = brand.query_all()
    if form.validate_on_submit():
        if request.method == 'POST':
            category_name = request.form['category_name']
            brand_id = request.form['brand_id']
            category_exist = category.find(category_name)
            if len(category_exist) == 0:
                return category.create(category_name, brand_id) and redirect('/category')
            else:
                error = "Your category is error"
    return render_template('CRUD/category/create.html', brands=brands, error=error, category_active="active", form=form)


@category_blueprint.route('/', methods=['POST'])
def edit_category():
    form = CategoryForm()
    category = CategoryModel()
    if form.validate_on_submit():
        category_id = request.form['category_id']
        category_name = request.form['category_name']
        brand_id = request.form['brand_id']
        result, error = category.edit(category_id, category_name, brand_id)
        if error:
            return list_category(error)
    return list_category(form=form)
