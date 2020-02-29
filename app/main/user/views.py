from flask import redirect, render_template, Blueprint, session, request, Request
from app.main.auth.views import login_required

user_blueprint = Blueprint(
    'user', __name__, template_folder='templates')


@user_blueprint.route('/', methods=['GET'])
@login_required
def profile():
    return render_template("profile.html", user=session['cur_user'])

@user_blueprint.route('/upload', methods=['POST'])
def upload():
    print("huhu")
    return render_template("profile.html", user=session['cur_user'])
