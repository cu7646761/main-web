from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import (DataRequired, Regexp, Length, Email)


class UpdatePswForm(FlaskForm):
    old_password = PasswordField(
        'old_password',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    new_password_1 = PasswordField(
        'new_password_1',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    new_password_2 = PasswordField(
        'new_password_2',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
