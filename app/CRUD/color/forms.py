from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import (DataRequired, Regexp, Length)


class ColorForm(FlaskForm):
    color_name = StringField(
        'color_name',
        [DataRequired(), Regexp(r'^[a-zA-Z\s]*$'), Length(min=4, max=25)]
    )
