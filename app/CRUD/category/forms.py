from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import (DataRequired, Regexp, Length)


class CategoryForm(FlaskForm):
    category_name = StringField(
        'category_name',
        [DataRequired(), Regexp(r'^[a-zA-Z0-9\s]*$'), Length(min=4, max=25)]
    )
