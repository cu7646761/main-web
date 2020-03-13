import os
import googlemaps
from datetime import datetime
from flask import redirect, render_template, Blueprint, session, request, jsonify

from app.main.address.models import AddressModel
from app.main.auth.models import UserModel
from app.main.auth.views import login_required
from werkzeug.utils import secure_filename

from app.main.category.models import CategoryModel
from app.main.user.forms import UpdatePswForm
from constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, LINK_IMG, LINK_IMG_AVATAR_DEF, SERVER_NAME, GENDER
from utils import Utils
from vietnam_provinces.enums.districts import ProvinceEnum, ProvinceDEnum, DistrictEnum, DistrictDEnum

user_blueprint = Blueprint(
    'user', __name__, template_folder='templates')

gmaps = googlemaps.Client(key='')

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
    return render_template("profile.html", user=session['cur_user'], error=error, form=form, success=success,
                           province_list=province_list, cate_list=cate.query_all())


@user_blueprint.route('/', methods=['POST'])
def upload(form=None):
    if 'file' not in request.files:
        return profile(error='No file part', form=form)
    file = request.files['file']
    if file.filename == '':
        return profile(error='No selected file', form=form)
    elif not allowed_file(file.filename):
        return profile(error='Format of your file is png, jpg, jpeg, gif')
    date_obj = datetime.now()
    file.filename = date_obj.strftime("%H:%M:%S.%f - %b %d %Y") + "-" + file.filename
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    user = UserModel()
    link_image_new = LINK_IMG + filename
    session['cur_user'].link_image = link_image_new
    res, error = user.update_link_image(session['cur_user'].email, link_image_new)
    if error:
        return profile(error=error, form=form)
    return redirect('/profile')


@user_blueprint.route('/delete-img', methods=['GET'])
def delete_image(form=None):
    link_img = session['cur_user'].link_image
    if link_img == LINK_IMG_AVATAR_DEF:
        return profile(error="You must upload your avatar before deleting", form=form)
    file_name = link_img[len(SERVER_NAME + '/static/images'):]
    os.remove(UPLOAD_FOLDER + file_name)
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
    res_address = request.form.get("result-address")
    love_cate = request.form.get("love_cate")
    district = request.form.get("district_edit")
    geocode_result = gmaps.geocode(res_address)
    latitude = geocode_result[0].get('geometry').get('location').get('lat')
    lngtitude = geocode_result[0].get('geometry').get('location').get('lng')
    address = AddressModel()
    print(district)
    current_user = None
    # address_id = address.find_by_detail(res_address)[0].id
    try: 
        if session['logged'] == True:
            current_user = session['cur_user']
    except:
        pass
    if current_user.address_id:
        print("KOKO")
        res, err = address.update(current_user.address_id, res_address, district, latitude, lngtitude)
    else:
        print("KKKKK")
        res, err = address.create(current_user.id, res_address, district, latitude, lngtitude)
    if err:
        return profile(error=err)
    love_cate = love_cate.split(',')
    list_obj_cate = []
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
        return profile(error=err, gender = gender, birthday = birthday)

    return profile(success="Your basic information is updated successfully", gender = gender, birthday = birthday)
