from flask import Blueprint, render_template, request, make_response, jsonify, redirect

from app import cache
from app.CRUD.color.forms import ColorForm
from app.CRUD.color.models import ColorModel
from constants import Pages

color_blueprint = Blueprint('color', __name__, template_folder='templates')


@color_blueprint.route('/api/list', methods=['GET'])
def list_color_api():
    page = request.args.get('page', 1, type=int)
    color = ColorModel()
    colors, total_pages = color.query_paginate(page)
    res = {
        "total_pages": total_pages,
        "data": [{"id": str(color.id), "name": color.value} for color in colors],
    }
    return make_response(jsonify(res), 200)


@color_blueprint.route('/', methods=['GET'])
@cache.cached(timeout=5)
def list_color(error=None, form=None):
    if form is None:
        form = ColorForm()
    page = request.args.get('page', 1, type=int)
    color = ColorModel()
    colors, total_pages = color.query_paginate(page)
    return render_template('CRUD/color/list.html', total_pages=total_pages, color_active="active", form=form, error=error, visible_page=Pages.VISIBLE_PAGE.value)


@color_blueprint.route('/create', methods=['GET', 'POST'])
def create_color(error=None):
    form = ColorForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            color_value = request.form['color_name']
            result, error = ColorModel.create(color_value)
            if error:
                return list_color(error)
            return redirect('/color')
    return render_template('CRUD/color/create.html', error=error, color_active="active", form=form)


@color_blueprint.route('/edit', methods=['POST'])
def edit_color():
    form = ColorForm()
    color = ColorModel()
    if form.validate_on_submit():
        color_id = request.form['color_id']
        color_value = request.form['color_name']
        result, error = color.edit(color_id, color_value)
        if error:
            return list_color(error)
    return list_color(form=form)
