import os
import googlemaps
from datetime import datetime
from flask import redirect, render_template, Blueprint, session, request, jsonify
from flask_mongoengine.wtf.fields import unicode
from werkzeug.datastructures import FileStorage

from app.model.address import AddressModel
from app.model.auth import UserModel
from app.main.auth.views import login_required
from werkzeug.utils import secure_filename

from app.model.category import CategoryModel
from app.main.user.forms import UpdatePswForm
from constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, LINK_IMG, LINK_IMG_AVATAR_DEF, SERVER_NAME
from utils import Utils
from vietnam_provinces.enums.districts import ProvinceEnum, DistrictEnum
from constants import API_KEY

from app.image.image_storage import delete_image_gc, upload_image_gc, get_size

user_blueprint = Blueprint(
    'user', __name__, template_folder='templates')

gmaps = googlemaps.Client(key=API_KEY)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user_blueprint.route('/district', methods=['GET'])
def get_district_by_city():
    city_id = request.args.get('city_id')
    district_list = list(DistrictEnum)
    dis_with_city = []
    for dis in district_list:
        if int(dis.province_code) == int(city_id):
            dis_with_city.append(dis)
    if not city_id:
        return jsonify({})
    return jsonify({'district': dis_with_city})


@user_blueprint.route('/', methods=['GET'])
@login_required
def profile(error=None, form=None, success=None):
    province_list = list(ProvinceEnum)
    cate = CategoryModel()
    if form is None:
        form = UpdatePswForm()

    addr = ""
    if session['cur_user'].address_id is None:
        addr = ""
    else:
        addr = session['cur_user'].address_id.detail

    category = CategoryModel()
    lst_cate_choose = [category.find_by_id(x.id)[0].name for x in session['cur_user'].favorite_categories]

    return render_template("profile.html", user=session['cur_user'], error=error, form=form, success=success,
                           province_list=province_list, cate_list=cate.query_all(), address=addr,
                           lst_cate_choose=lst_cate_choose)


@user_blueprint.route('/', methods=['POST'])
def upload(form=None):
    if 'file' not in request.files:
        return profile(error='No file part', form=form)
    file = request.files['file']
    if file.filename == '':
        return profile(error='No selected file', form=form)
    elif not allowed_file(file.filename):
        return profile(error='Format of your file is jpg')

    if session['cur_user'].link_image != LINK_IMG_AVATAR_DEF:
        image_name = session['cur_user'].link_image.replace("https://storage.googleapis.com/bloganuong_images/", "")
        res = delete_image_gc('bloganuong_images', image_name)
        if res is False:
            return profile(error="Error when deleting your image", form=form)

    date = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    name = file.filename.split('.')[0]
    ext = file.filename.split('.')[1]
    file.filename = name + "__" + date + "." + ext
    if int(get_size(file)) > 150000:
        return profile(error="Your image must be smaller than 150 KB")
    link_file = upload_image_gc('bloganuong_images', image_file=file)
    user = UserModel()

    session['cur_user'].link_image = link_file
    res, error = user.update_link_image(session['cur_user'].email, link_file)
    if error:
        return profile(error=error, form=form)
    return redirect('/profile')


@user_blueprint.route('/delete-img', methods=['GET'])
def delete_image(form=None):
    link_img = session['cur_user'].link_image
    if link_img == LINK_IMG_AVATAR_DEF:
        return profile(error="You must upload your avatar before deleting", form=form)
    image_name = session['cur_user'].link_image.replace("https://storage.googleapis.com/bloganuong_images/", "")
    res = delete_image_gc('bloganuong_images', image_name)
    if res is False:
        return profile(error="Error when deleting your image", form=form)
    session['cur_user'].link_image = LINK_IMG_AVATAR_DEF
    user = UserModel()
    res, error = user.update_link_image(session['cur_user'].email, LINK_IMG_AVATAR_DEF)
    if error:
        return profile(error=error, form=form)
    return redirect('/profile')


@user_blueprint.route('/update_pass', methods=['POST'])
def update_password(error=None):
    form = UpdatePswForm()
    if form.validate_on_submit():
        user = UserModel()
        email = session['cur_user'].email
        old_password = request.form.get("old_password")
        new_password_1 = request.form.get("new_password_1")
        new_password_2 = request.form.get("new_password_2")

        if new_password_1 != new_password_2:
            error = "Repeat password is incorrect"

        _user = user.find_by_email(email)[0]

        if not Utils.check_password(old_password, _user.password):
            error = "Incorrect password"

        if error is None:
            hashed_passwd = Utils.hash_password(new_password_1)
            new_user, error = user.update_psw(email, hashed_passwd.decode())
            if error:
                return profile(error=error, form=form)
            return profile(error=error, form=form, success="Your password is updated")
    return profile(error=error, form=form)


@user_blueprint.route('/update-basic', methods=['POST'])
def update_basic(error=None, form=None):
    if form is None:
        form = UpdatePswForm()

    birthday = request.form.get("birthday")
    gender = request.form.get("gender")
    res_address = request.form.get("result_address")
    love_cate = request.form.getlist("love_cate")
    district = res_address.split(',')[1]
    geocode_result = gmaps.geocode(res_address)
    latitude = str(geocode_result[0].get('geometry').get('location').get('lat'))
    longtitude = str(geocode_result[0].get('geometry').get('location').get('lng'))
    address = AddressModel()
    current_user = None

    try:
        if session['logged'] == True:
            current_user = session['cur_user']
    except:
        pass
    if current_user.address_id:
        res, err = address.update(current_user.address_id.id, res_address, district, latitude, longtitude)
    else:
        res, err = address.create(current_user.id, res_address, district, latitude, longtitude)
    if err:
        return profile(error=err)

    list_obj_cate = []
    if love_cate == "":
        list_obj_cate = session['cur_user'].favorite_categories
    else:
        category = CategoryModel()
        if isinstance(love_cate, str):
            list_obj_cate.append(category.find_by_name(love_cate)[0].id)
        else:
            for cate in love_cate:
                list_obj_cate.append(category.find_by_name(cate)[0].id)

    user = UserModel()
    email = session['cur_user'].email
    if gender == 'Nam':
        gender = 0
    elif gender == 'Nữ':
        gender = 1
    else:
        gender = 2
    result, err = user.update_basic(email, birthday, gender, list_obj_cate)
    if err:
        return profile(error=err)

    user = UserModel()
    cur_user = user.find_by_id(session['cur_user'].id)[0]
    session['cur_user'] = cur_user

    return profile(success="Cập nhật thông tin thành công.")
