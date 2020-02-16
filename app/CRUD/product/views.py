from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for

from app import cache
from app.CRUD.product.forms import ProductForm
from app.CRUD.brand.models import BrandModel
from app.CRUD.product.models import ProductModel
from app.CRUD.category.models import CategoryModel
from constants import Pages

product_blueprint = Blueprint('product', __name__, template_folder='templates')


@product_blueprint.route('/create', methods=['POST', 'GET'])
def create_product():
    form = ProductForm()
    brand = BrandModel()
    list_brand = brand.query_all()
    if form.validate_on_submit():
        if request.method == 'POST':
            category_id = request.form.get('select-category')
            name = request.form.get('product_name')
            result, error = ProductModel.create(category_id, name)
            if error:
                return render_template('CRUD/product/create.html', list_brand=list_brand, product_active="active",
                                       form=form, error=error)
            return redirect('/product')
    return render_template('CRUD/product/create.html', list_brand=list_brand, product_active="active", form=form)


@product_blueprint.route('/category', methods=['GET'])
def get_category_by_brand():
    brand_id = request.args.get('brand_id')
    category = CategoryModel()
    if not brand_id:
        return jsonify({})
    categories = category.query_by_brand_id(brand_id)
    jsonable_category = [{'id': str(category.id), 'name': category.name}
                         for category in categories]
    return jsonify(jsonable_category)


@product_blueprint.route('/', methods=['GET'])
@cache.cached(timeout=5)
def list_products(error=None, form=None):
    if form is None:
        form = ProductForm()
    product = ProductModel()
    page = request.args.get("page", 1, type=int)
    products_pagination, total_page, current_page = product.query_paginate(page)
    brand_all = BrandModel()
    products = []
    for product in products_pagination:
        brand = BrandModel()
        category = CategoryModel()
        category_s = category.find_by_id(product.category_id)
        brand_s = brand.find_by_id(category_s[0].brand_id)
        res = {'brand': brand_s[0].name, 'brand_id': brand_s[0].id,
               'category': category_s[0].name, 'category_id': product.category_id,
               'name': product.name, 'id': str(product.id)}
        products.append(res)
    list_brand = brand_all.query_all()
    return render_template('CRUD/product/list.html', products=products, total_page=total_page,
                           current_page=current_page, list_brand=list_brand, product_active="active", form=form,
                           error=error, visible_page=Pages.VISIBLE_PAGE.value)


@product_blueprint.route('/', methods=['POST'])
def edit_product():
    form = ProductForm()
    product = ProductModel()
    if form.validate_on_submit():
        product_id = request.form.get('product_id', None)
        category_id = request.form.get('category_id')
        product_name = request.form.get('product_name')
        result, error = product.edit(product_id, category_id, product_name)
        if error:
            return list_products(error)
    return list_products(form=form)
