from functools import wraps
from flask import redirect, render_template, Blueprint, session, request
from app.main.auth.models import UserModel

from utils import Utils

auth_blueprint = Blueprint(
    'auth', __name__, template_folder='templates')


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # if user is not logged in, redirect to login page
        if not session.get('logged'):
            return redirect("/login")
        return f(*args, **kwargs)
    return wrap


@auth_blueprint.route("/login", methods=["GET"])
def get_login():
    return render_template('login.html')


@auth_blueprint.route("/signup", methods=["GET"])
def get_signup():
    return render_template('signup.html')


@auth_blueprint.route("/signup", methods=["POST"])
def post_signup(error=None):
    user = UserModel()

    email = request.form.get("email", "")
    password = request.form.get("password", "")

    if not email:
        error = "Email is required"
    elif not password:
        error = "Password is required"
    elif len(user.find_by_email(email)) == 1:
        error = "User {0} is already registered.".format(email)

    if error is None:
        # the name is available, store it in the database
        hashed_passwd = Utils.hash_password(password)

        new_user, error = UserModel.create(email, hashed_passwd)
        if error:
            return render_template('signup.html', error=error, success=None)
        return render_template('signup.html', error=error, success="You have signed up successfully")

    return render_template('signup.html', error=error)


@auth_blueprint.route('/login', methods=['POST'])
def post_login(error=None):
    user = UserModel()

    email = request.form.get("email", "")
    plain_text_password = request.form.get("password", "")

    user = user.find_by_email(email)

    if len(user) == 0:
        error = "Incorrect email or password"
    elif not Utils.check_password(plain_text_password, user[0].password):
        error = "Incorrect password"

    if error is None:
        session['logged'] = True
        session['cur_user'] = user

        return redirect('/')

    return render_template("login.html", error=error)


@auth_blueprint.route("/logout", methods=["GET"])
def get_logout():
    session.clear()
    return redirect('/login')


@auth_blueprint.route('/', methods=['GET'])
@login_required
def home():
    return render_template("index.html")
