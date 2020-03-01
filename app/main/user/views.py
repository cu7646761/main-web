import os

from flask import redirect, render_template, Blueprint, session, request, Request, flash
from app.main.auth.views import login_required
from werkzeug.utils import secure_filename
from constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from flask import send_from_directory

user_blueprint = Blueprint(
    'user', __name__, template_folder='templates')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user_blueprint.route('/', methods=['GET'])
@login_required
def profile():
    return render_template("profile.html", user=session['cur_user'])


@user_blueprint.route('/upload', methods=['POST'])
def upload():
    print("huhu")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            print(filename)



            return redirect(request.url)
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
