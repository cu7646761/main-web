from functools import wraps
from flask import redirect, render_template, Blueprint, session, request

from app.main.auth.forms import LoginForm, SignupForm, EmailForm, ResetForm
from app.model.auth import UserModel
from app.model.store import StoreModel
from app.main.search.forms import SearchForm

from app.email import send_email
from constants import SERVER_NAME
from flask.helpers import make_response
from flask.json import jsonify
from constants import API_KEY, CATE_LIST
from utils import Utils

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
    return render_template('login.html', form=form, footer="footer")


@auth_blueprint.route("/signup", methods=["GET"])
def get_signup():
    form = SignupForm()
    return render_template('signup.html', form=form, footer="footer")


@auth_blueprint.route("/signup", methods=["POST"])
def post_signup(error=None):
    form = SignupForm()
    if form.validate_on_submit():
        user = UserModel()
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")
        if not email:
            error = "Vui lòng nhập email"
        elif not password:
            error = "Vui lòng nhập mật khẩu"
        elif password != password_confirm:
            error = "Mật khẩu lặp lại không đúng"

        elif len(user.find_by_email(email)) == 1:
            if user.find_by_email(email)[0].active == 1:
                error = "Người dùng đã được đăng ký".format(email)
            elif user.find_by_email(email)[0].active == 0:
                try:
                    url = str(SERVER_NAME) + "/confirm-email?email=" + str(email) + "&password=" + str(
                        user.find_by_email(email)[0].password)
                    message = "Bạn đã đăng nhập vào hệ thống <strong>BlogAnUong</strong>.<br> Để hoàn tất đăng nhập xin bạn hãy truy cập vào đường link sau:" + url
                    res = send_email(subject="Xác nhận đăng nhập vào BlogAnUong",
                                     html_content=message,
                                     recipients=str(email))
                    return render_template('signup.html',
                                           success="Tài khoản chưa được kích hoạt. Vui lòng kiểm tra email và hoàn tất thủ tục đăng ký",
                                           form=form, footer="footer")
                except Exception as e:
                    print(str(e))
        if error is None:
            # the name is available, store it in the database
            hashed_passwd = Utils.hash_password(password)
            new_user, error = UserModel.create(email, hashed_passwd, 0)

            try:
                url = str(SERVER_NAME) + "/confirm-email?email=" + str(email) + "&password=" + str(hashed_passwd)[2:]
                message = "Bạn đã đăng nhập vào hệ thống <strong>BlogAnUong</strong>.<br> Để hoàn tất đăng nhập xin bạn hãy truy cập vào đường link sau:" + url
                res = send_email(subject="Xác nhận đăng nhập vào BlogAnUong", html_content=message,
                                 recipients=str(email))
            except Exception as e:
                print(str(e))

            if error:
                return render_template('signup.html', error=error, success=None, form=form, footer="footer")

            return render_template('signup.html',
                                   success="Tài khoản chưa được kích hoạt. Vui lòng kiểm tra email và hoàn tất thủ tục đăng ký",
                                   form=form, footer="footer")
    return render_template('signup.html', error=error, form=form, footer="footer")


@auth_blueprint.route('/confirm-email', methods=['GET'])
def get_confirm_email(error=None):
    email = request.args.get('email')
    hashed_password = request.args.get('password')

    user = UserModel()
    user_1 = user.find_by_email(email)

    if hashed_password == user_1[0].password:
        user_active, error = user.turn_on_acc(email)
        if error:
            print(error)
    return redirect('/login')


@auth_blueprint.route('/login', methods=['POST'])
def post_login(error=None):
    form = LoginForm()
    if form.validate_on_submit():
        _user = UserModel()
        email = request.form.get("email", "")
        plain_text_password = request.form.get("password", "")
        user = _user.find_by_email(email)
        if len(user) == 0:
            error = "Email hoặc mật khẩu không chính xác"
        elif not Utils.check_password(plain_text_password, user[0].password):
            error = "Mật khẩu không chính xác"
        elif user[0].active == 0:
            error = "Tài khoản chưa được kích hoạt. Vui lòng kiểm tra email và hoàn tất thủ tục đăng ký"
        if error is None:
            session.permanent = True
            session['logged'] = True
            session['cur_user'] = user[0]
            session['search'] = ""
            session['search_tsl'] = ""
            session['recommendation'] = ""
            if user[0].active == 2:
                return redirect('/admin/')
            return redirect('/')
    return render_template("login.html", error=error, form=form, footer="footer")


@auth_blueprint.route("/logout", methods=["GET"])
def get_logout():
    session.clear()
    return redirect('/login')


@auth_blueprint.route('/', methods=['GET'])
@login_required
def home(form=None):
    session["pos"] = None
    if form is None:
        form = SearchForm()
    store = StoreModel().find_by_id
    return render_template("index.html", user=session['cur_user'], form=form, API_KEY=API_KEY)


@auth_blueprint.route('/forget-password', methods=['GET', 'POST'])
def forget_password(form=None):
    form = EmailForm()
    if form.validate_on_submit():
        _user = UserModel()
        email = request.form.get("email", "")
        user = _user.find_by_email(email)
        if len(user) == 0:
            error = "Email không chính xác"
            return render_template("forget-password.html", form=form, error=error, footer="footer")
        try:
            url = str(SERVER_NAME) + "/reset-password/user_id=" + str(user[0].id)
            message = "Bạn đã yêu cầu reset mật khẩu trong hệ thống <strong>BlogAnUong</strong>.<br> Để hoàn tất reset mật khẩu, xin bạn hãy truy cập vào đường link sau:" + url
            res = send_email(subject="Xác nhận reset mật khẩu BlogAnUong",
                             html_content=message,
                             recipients=str(email))
            return render_template("forget-password.html", form=form, success="Vui lòng kiểm tra email để lấy lại mật khẩu.", footer="footer")
        except Exception as e:
            print(str(e))
    return render_template("forget-password.html", form=form, footer="footer")


@auth_blueprint.route('/reset-password/<string:user_id>', methods=['GET'])
def reset_password(form=None, user_id=None):
    print(user_id)
    form = ResetForm()
    _id = user_id.split("=")[1]
    return render_template("reset-password.html", form=form, user_id=_id, footer="footer")

@auth_blueprint.route('/reset-password', methods=['POST'])
def post_reset_password(form=None, user_id=None, error=None):
    form = ResetForm()
    user = UserModel()
    user_id = request.form.get("user_id", "")
    email = user.find_by_id(user_id)[0].email
    password = request.form.get("password", "")
    password_confirm = request.form.get("password_confirm", "")
    if not password:
        error = "Vui lòng nhập mật khẩu"
    elif password != password_confirm:
        error = "Mật khẩu lặp lại không đúng"
    if error is None:
        hashed_passwd = Utils.hash_password(password_confirm)
        new_user, error = user.update_psw(email, hashed_passwd.decode())
        if error:
            return render_template('reset-password.html', error=error, form=form, footer="footer", user_id=user_id)
        return render_template('reset-password.html', success="Tài khoản đã được đổi mật khẩu thành công", form=form,
                               footer="footer", user_id=user_id)
    return render_template('reset-password.html', error=error, form=form, footer="footer", user_id=user_id)


@auth_blueprint.route('/about-us', methods=['GET'])
@login_required
def about_us(form=None):
    return render_template("about-us.html", user=session['cur_user'])


@auth_blueprint.route('/contact-us', methods=['GET'])
@login_required
def contact_us(form=None):
    return render_template("contact-us.html", user=session['cur_user'])


@auth_blueprint.route('/load-predict-cate', methods=['GET'])
@login_required
def load_predict_cate():
    print(session["search_tsl"])
    if session["search"]:
        print(session['search'])
        tsl = Utils.sample_translate_text(session["search"], "en-US", "britcat3")
        session["search"] = ""
        text = tsl.translations[0].translated_text.lower()
        session["search_tsl"] += text + " "
        print(session["search_tsl"])
        rs = Utils.predict_food_cate_online(session["search_tsl"])
        rs.pop('other', None)
        session['recommendation'] = rs
        print(rs)
        # if rs:
        #     res = make_response(jsonify(rs), 201)
        #     return res
    elif session["search_tsl"]:
        if session['recommendation']:
            res_dict = {}
            rs_list = session['recommendation'].items()
            print(rs_list)
            for k, v in rs_list:
                res_dict[k] = CATE_LIST[k]
            # res_dict = {k: v for k, v in sorted(res_dict.items(), key=lambda item: item[1], reverse=True)}
            res = make_response(jsonify(res_dict), 201)
            print(res.data)
            return res

    res = make_response(jsonify({}), 200)
    return res


@auth_blueprint.route('/reset-rec')
@login_required
def reset_rec():
    rp = request.args.get('rp', '', type=str)
    if rp != 'n':
        cur_user = UserModel().find_by_id(session['cur_user'].id)[0]
        data_update = cur_user.infor_rec + " " + session['search_tsl']
        cur_user.update(set__infor_rec=data_update)
        session['search_tsl'] = ""
        return redirect('/stores/?cate_predict=' + rp)
    elif rp == 'n':
        session['search_tsl'] = ""
        return make_response(jsonify({}), 200)


@auth_blueprint.route('/load_geo_places')
@login_required
def load_geo_places():
    stores = StoreModel().query_all()
    datas = []
    for store in stores:
        # address = AddressModel().find_by_id(store.address_id)[0]
        datas += [{
            "lng": float(store.position["lng"]),
            "lat": float(store.position["lat"]),
            "id": str(store.id),
            "name": store.name,
            "link_img": store.link_image[0]
        }]
    res = make_response(jsonify(datas), 200)
    return res


@auth_blueprint.route("/load_geolocation")
def load_geolocation():
    if request.args:
        pos = {
            "lat": request.args.get("lat"),
            "lng": request.args.get("lng")
        }
        session["pos"] = pos
    res = make_response(jsonify({"message": "OK"}), 200)
    return res
