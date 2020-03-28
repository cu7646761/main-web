from flask_wtf import FlaskForm
from wtforms import PasswordField, validators
from wtforms.validators import (DataRequired, Regexp, Length, Email)
from wtforms.fields.simple import SubmitField
from wtforms.fields.core import StringField, RadioField
from wtforms.widgets import TextArea


class AddCommentForm(FlaskForm):
    comment = StringField("comment", widget=TextArea())