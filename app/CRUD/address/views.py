from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for

from app import cache
from app.CRUD.address.forms import AddressForm
from app.CRUD.city.models import CityModel
from app.CRUD.address.models import AddressModel
from app.CRUD.district.models import DistrictModel

from constants import Pages

address_blueprint = Blueprint('address', __name__, template_folder='templates')


@address_blueprint.route('/create', methods=['POST', 'GET'])
def create_address():
    form = AddressForm()
    city = CityModel()
    list_city = city.query_all()
    if form.validate_on_submit():
        if request.method == 'POST':
            district_id = request.form.get('select-district')
            detail = request.form.get('address_name')
            result, error = AddressModel.create(district_id, detail)
            if error:
                return render_template('CRUD/address/create.html', list_city=list_city, address_active="active",
                                       form=form, error=error)
            return redirect('/address')
    return render_template('CRUD/address/create.html', list_city=list_city, address_active="active", form=form)


@address_blueprint.route('/district', methods=['GET'])
@cache.cached(timeout=5)
def get_district_by_city():
    city_id = request.args.get('city_id')
    district = DistrictModel()
    if not city_id:
        return jsonify({})
    districts = district.query_by_city_id(city_id)
    jsonable_district = [{'id': str(district.id), 'name': district.name}
                         for district in districts]
    return jsonify(jsonable_district)


@address_blueprint.route('/', methods=['GET'])
def list_addresses(error=None, form=None):
    if form is None:
        form = AddressForm()
    address = AddressModel()
    page = request.args.get("page", 1, type=int)
    addresses_pagination, total_page, current_page = address.query_paginate(page)
    city_all = CityModel()
    addresses = []
    for address in addresses_pagination:
        city = CityModel()
        district = DistrictModel()
        district_s = district.find_by_id(address.district_id)
        city_s = city.find_by_id(district_s[0].city_id)
        res = {'city': city_s[0].name, 'city_id': city_s[0].id,
               'district': district_s[0].name, 'district_id': address.district_id,
               'detail': address.detail, 'id': str(address.id)}
        addresses.append(res)
    list_city = city_all.query_all()
    return render_template('CRUD/address/list.html', addresses=addresses, total_page=total_page,
                           current_page=current_page, list_city=list_city, address_active="active", form=form,
                           error=error, visible_page=Pages.VISIBLE_PAGE.value)


@address_blueprint.route('/', methods=['POST'])
def edit_address():
    form = AddressForm()
    address = AddressModel()
    if form.validate_on_submit():
        address_id = request.form.get('address_id', None)
        district_id = request.form.get('district_id')
        address_detail = request.form.get('address_name')
        result, error = address.edit(address_id, district_id, address_detail)
        if error:
            return list_addresses(error)
    return list_addresses(form=form)
