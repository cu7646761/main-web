from functools import wraps
from flask import redirect, render_template, Blueprint, session, request

from app.main.store.forms import StoreForm
from app.main.store.models import StoreModel

from utils import Utils

store_blueprint = Blueprint(
    'store', __name__, template_folder='templates')

@store_blueprint.route("/detail-store", methods=["GET"])
def view_detail():
    form = StoreForm()
    store = StoreModel()
    StoreModel.create("huhu", "123")
    print(store.query_all())
    return render_template('detail.html', form=form)

# @auth_blueprint.route("/detail-store", methods=["POST"])
# def post_signup(error=None):
#     form = DetailStoreForm()
#     if form.validate_on_submit():
#         user = StoreModel()
#         email = request.form.get("email", "")
#         password = request.form.get("password", "")
#         if not email:
#             error = "Email is required"
#         elif not password:
#             error = "Password is required"
#         elif len(user.find_by_email(email)) == 1:
#             error = "Store {0} is already registered.".format(email)
#         if error is None:
#             # the name is available, store it in the database
#             hashed_passwd = Utils.hash_password(password)
#             new_user, error = StoreModel.create(email, hashed_passwd)
#             if error:
#                 return render_template('signup.html', error=error, success=None, form=form)
#             return render_template('signup.html', success="You have signed up successfully", form=form)
#     return render_template('signup.html', error=error, form=form)


