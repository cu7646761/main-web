from flask import Blueprint, render_template, redirect, request, jsonify

from app.main.search.forms import SearchForm
from app.CRUD.address.models import AddressModel
from app.CRUD.city.models import CityModel
from app.CRUD.district.models import DistrictModel
from app.main.user.models import UserModel
from app.main.search.models import FullTextSearch, FuzzySearch, SuggestionSearch

search_blueprint = Blueprint('search', __name__, template_folder='templates')


@search_blueprint.route('/full-text', methods=['GET'])
def full_text():
    form = SearchForm()
    if not form.validate() or not form.q.data:
        return redirect('/register')
    cls_model = [AddressModel, CityModel, DistrictModel]
    reindex_all = [model.reindex() for model in cls_model]
    # reindex_all = CityModel.reindex()
    kind_search = FullTextSearch()
    search_model = [model.search(form.q.data, 1, 10, kind_search) for model in cls_model]
    search_obj = []
    for obj, total in search_model:
        if not isinstance(total, int):
            search_obj.extend(total)
    return render_template('CRUD/search/list.html', search_obj=search_obj, form=form)


@search_blueprint.route('/fuzzy', methods=['GET'])
def fuzzy():
    form = SearchForm()
    if not form.validate() or not form.q.data:
        return redirect('/city')
    cls_model = [UserModel]
    reindex_all = [model.reindex() for model in cls_model]
    kind_search = FuzzySearch()
    search_model = [model.search(form.q.data, 1, 10, kind_search) for model in cls_model]
    search_obj = []
    for obj, total in search_model:
        if not isinstance(total, int):
            search_obj.extend(total)
    return render_template('CRUD/search/fuzzy.html', search_obj=search_obj, form=form)


@search_blueprint.route('/suggestion', methods=['POST'])
def suggestion():
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
