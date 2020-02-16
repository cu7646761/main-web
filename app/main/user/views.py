from flask import flash, redirect, render_template, Blueprint, request
from app.main.user.oauth import OAuthSignIn
from .forms import RegisterForm
from app.main.user.models import UserModel

user_blueprint = Blueprint(
    'user', __name__, template_folder='templates')


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    user = UserModel()
    if form.validate_on_submit():
        if request.method == 'POST':
            email = form.email.data
            user_exist_fb = user.find_by_email(email)
            if len(user_exist_fb) == 0:
                result, error = UserModel.create(email, form.password.data)
                if error:
                    flash(error)
                flash('You sign up successfully. ')
            else:
                flash('Your email have already signed up.')
    return render_template('index.html', form=form)

# @user_blueprint.route('/authorize/<provider>')
# def oauth_authorize(provider):
#     oauth = OAuthSignIn.get_provider(provider)
#     return oauth.authorize()
#
#
# @user_blueprint.route('/callback/<provider>')
# def oauth_callback(provider):
#     oauth = OAuthSignIn.get_provider(provider)
#     id_social, email = oauth.callback()
#     user_exist = User.query.filter_by(email=email).first()
#     if (user_exist is None) and (email is not None):
#         user = User(
#             email=email,
#             email_fb=email if provider == "facebook" else None,
#             email_tw=email if provider == "twitter" else None,
#             id_fb=id_social if provider == "facebook" else None,
#             id_tw=id_social if provider == "twitter" else None)
#         db.session.add(user)
#         db.session.commit()
#         flash('You sign up ' + provider + ' successful. ')
#     else:
#         flash('You have already signed up ' + provider + '.')
#     return redirect('/register')
