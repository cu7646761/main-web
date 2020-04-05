from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import (DataRequired, Regexp, Length, Email)


class CommentForm(FlaskForm):
    pass
