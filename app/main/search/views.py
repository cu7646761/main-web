from flask import Blueprint, render_template, redirect, request, jsonify, session

from app.main.search.forms import SearchForm
from app.main.search.models import FullTextSearch, SuggestionSearch
from app.main.store.models import StoreModel

search_blueprint = Blueprint('search', __name__, template_folder='templates')


@search_blueprint.route('/full-text', methods=['GET'])
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

    print(search_obj)
    return render_template('index.html', search_obj=search_obj, form=form, user=session['cur_user'])


# @search_blueprint.route('/fuzzy', methods=['GET'])
# def fuzzy():
#     form = SearchForm()
#     if not form.validate() or not form.q.data:
#         return redirect('/city')
#     cls_model = [UserModel]
#     reindex_all = [model.reindex() for model in cls_model]
#     kind_search = FuzzySearch()
#     search_model = [model.search(form.q.data, 1, 10, kind_search) for model in cls_model]
#     search_obj = []
#     for obj, total in search_model:
#         if not isinstance(total, int):
#             search_obj.extend(total)
#     return render_template('CRUD/search/fuzzy.html', search_obj=search_obj, form=form)


@search_blueprint.route('/suggestion', methods=['POST'])
def suggestion():
    search_term = request.data.decode("utf-8").split("=")[1]
    cls_model = [StoreModel]
    # reindex_all = [model.reindex() for model in cls_model]
    kind_search = SuggestionSearch()
    search_model = [model.search(search_term, 1, 10, kind_search) for model in cls_model]
    search_obj = []
    for obj, total in search_model:
        if not isinstance(total, int):
            search_obj.extend(total)

    return jsonify({"data": search_obj})
