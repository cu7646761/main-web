from functools import wraps
from flask import redirect, render_template, Blueprint, session, request, Request

from app.main.auth.forms import LoginForm, SignupForm
from app.main.auth.models import UserModel

from app.email import send_email
from utils import Utils
from constants import SERVER_NAME

auth_blueprint = Blueprint(
    'auth', __name__, template_folder='templates')


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            # if user is not logged in, redirect to login page
            if not session['logged']:
                return redirect("/login")
        except:
            return redirect("/login")
        return f(*args, **kwargs)

    return wrap


@auth_blueprint.route("/login", methods=["GET"])
def get_login():
    form = LoginForm()
    return render_template('login.html', form=form)


@auth_blueprint.route("/signup", methods=["GET"])
def get_signup():
    form = SignupForm()
    return render_template('signup.html', form=form)


@auth_blueprint.route("/signup", methods=["POST"])
def post_signup(error=None):
    form = SignupForm()
    if form.validate_on_submit():
        user = UserModel()
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")
        if not email:
            error = "Email is required"
        elif not password:
            error = "Password is required"
        elif password != password_confirm:
            error = "Repeat password is incorrect"

        elif len(user.find_by_email(email)) == 1:
            error = "User {0} is already registered.".format(email)
        if error is None:
            # the name is available, store it in the database
            hashed_passwd = Utils.hash_password(password)
            new_user, error = UserModel.create(email, hashed_passwd, 0)

            try:
                url = str(SERVER_NAME) + "/confirm-email?email=" + str(email) + "&password=" + str(hashed_passwd)
                message = "Bạn đã đăng nhập vào hệ thống BlogAnUong. Để hoàn tất đăng nhập xin bạn hãy truy cập vào đường xin sau:" + url
                send_email(subject="Xác nhận đăng nhập vào BlogAnUong",
                           text_body=message,
                           recipients=[str(email)])
            except Exception as e:
                print(str(e))

            if error:
                return render_template('signup.html', error=error, success=None, form=form)

            return render_template('signup.html',
                                   success="You account is not activated. Please check email and confirm email to complete sign up",
                                   form=form)
    return render_template('signup.html', error=error, form=form)


@auth_blueprint.route('/confirm-email', methods=['GET'])
def get_confirm_email(error=None):
    email = request.args.get('email')
    hashed_password = request.args.get('password')

    user = UserModel()
    user_1 = user.find_by_email(email)

    if hashed_password[2:] == user_1[0].password:
        user_active, error = user.turn_on_acc(email)
        if error:
            print(error)
    return redirect('/login')


@auth_blueprint.route('/login', methods=['POST'])
def post_login(error=None):
    form = LoginForm()

    if form.validate_on_submit():
        user = UserModel()
        email = request.form.get("email", "")
        plain_text_password = request.form.get("password", "")

        user = user.find_by_email(email)

        if len(user) == 0:
            error = "Incorrect email or password"
        elif not Utils.check_password(plain_text_password, user[0].password):
            error = "Incorrect password"
        elif user[0].active == 0:
            error = "You account is not activated. Please check email and confirm email to complete sign up"
        if error is None:
            session['logged'] = True
            session['cur_user'] = user
            return redirect('/')
    return render_template("login.html", error=error, form=form)


@auth_blueprint.route("/logout", methods=["GET"])
def get_logout():
    session.clear()
    return redirect('/login')


@auth_blueprint.route('/', methods=['GET'])
@login_required
def home():
    return render_template("index.html")
