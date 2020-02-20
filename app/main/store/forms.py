from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import (DataRequired, Regexp, Length, Email)


class StoreForm(FlaskForm):
    email = EmailField(
        'email',
        [DataRequired(), Regexp(r'[^@]+@[^@]+\.[^@]+'), Length(min=4, max=25)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
