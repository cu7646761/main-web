from flask import Blueprint, render_template, current_app, request, jsonify, redirect, url_for, make_response

from app import cache
from app.CRUD.district.forms import DistrictForm
from app.CRUD.city.models import CityModel
from app.CRUD.district.models import DistrictModel
from constants import Pages

district_blueprint = Blueprint(
    'district', __name__, template_folder='templates')


@district_blueprint.route('/api/list', methods=['GET'])
def list_district_api():
    district = DistrictModel()
    city = CityModel()
    page = request.args.get('page', 1, type=int)
    districts, total_pages = district.query_paginate(page)
    res = {
        "total_pages": total_pages,
        "data": [{"id": str(district.id), 'city_name': city.get_name_by_id(district.city_id), "name": district.name} for
                 district in districts],
    }
    return make_response(jsonify(res), 200)


@district_blueprint.route('/', methods=['GET'])
@cache.cached(timeout=5)
def list_district(error=None, form=None):
    city = CityModel()
    if form is None:
        form = DistrictForm()
    district = DistrictModel()
    page = request.args.get('page', 1, type=int)
    districts, total_pages = district.query_paginate(page)
    cities = city.query_all()
    return render_template('CRUD/district/list.html', total_pages=total_pages, cities=cities, district_active="active",
                           form=form, visible_page=Pages.VISIBLE_PAGE.value)


@district_blueprint.route('/create', methods=['GET', 'POST'])
def create_district(error=None):
    form = DistrictForm()
    city = CityModel()
    district = DistrictModel()
    cities = city.query_all()
    if form.validate_on_submit():
        if request.method == 'POST':
            district_name = request.form['district_name']
            city_id = request.form['city_id']
            district_exist = district.find(district_name)
            if len(district_exist) == 0:
                return district.create(district_name, city_id) and redirect('/district')
            else:
                error = "Your district is error"
    return render_template('CRUD/district/create.html', cities=cities, error=error, district_active="active", form=form)


@district_blueprint.route('/', methods=['POST'])
def edit_district():
    form = DistrictForm()
    district = DistrictModel()
    if form.validate_on_submit():
        district_id = request.form['district_id']
        district_name = request.form['district_name']
        city_id = request.form['city_id']
        result, error = district.edit(district_id, district_name, city_id)
        if error:
            return list_district(error)
    return list_district(form=form)
