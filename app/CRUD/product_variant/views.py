from flask import Blueprint, render_template, request, jsonify, redirect, url_for

from app import cache
from app.CRUD.address.models import AddressModel
from app.CRUD.product_variant.models import ProductVariantModel
from app.CRUD.store.models import StoreModel
from app.CRUD.product.models import ProductModel
from app.CRUD.color.models import ColorModel
from constants import Pages

variant_blueprint = Blueprint(
    'variant', __name__, template_folder='templates')


@variant_blueprint.route('/', methods=['GET'])
@cache.cached(timeout=5)
def index():
    page = request.args.get("page", 1, type=int)
    product_variant = ProductVariantModel()
    store = StoreModel()
    product = ProductModel()
    color = ColorModel()
    stores = store.query_all()
    products = product.query_all()
    colors = color.query_all()
    product_variants, total_pages, cur_page = product_variant.query_paginate(page)
    return render_template('CRUD/product_variant/list.html', stores=stores, products=products, colors=colors,
                           variant_active="active", variants=product_variants, pages=total_pages, visible_page=Pages.VISIBLE_PAGE.value)


@variant_blueprint.route('/api/create', methods=['POST'])
def api_create():
    price = request.values.get("product_variant_price")
    product_id = request.values.get("product_id", None)
    store_id = request.values.get("store_id", None)
    color_id = request.values.get("color_id", None)
    if not product_id or not store_id or not color_id:
        return redirect(url_for("variant.create"))
    result, error = ProductVariantModel.create(price, product_id, store_id, color_id)
    if error:
        return redirect(url_for("variant.create"))
    return redirect(url_for("variant.index"))


@variant_blueprint.route('/api/edit', methods=['POST'])
def api_edit():
    data = request.get_json()
    product_variant = ProductVariantModel()
    _id = data.get("id", None)
    price = data.get("price", 0)
    product_id = data.get("product_id", None)
    store_id = data.get("store_id", None)
    color_id = data.get("color_id", None)

    if product_id is None or store_id is None or id is None or color_id is None:
        return jsonify({"success": False, "data": None})
    result, error = product_variant.edit(_id, price, product_id, store_id, color_id)
    if error:
        return redirect(url_for("variant.index"))
    return jsonify({"success": True})


@variant_blueprint.route("/create")
def create():
    store = StoreModel()
    product = ProductModel()
    color = ColorModel()
    address = AddressModel()
    stores = store.query_all()
    products = product.query_all()
    colors = color.query_all()
    addresses = address.query_all()
    return render_template("CRUD/product_variant/create.html", stores=stores, products=products, colors=colors, addresses=addresses)
