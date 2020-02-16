from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import (DataRequired, Regexp, Length)


class AddressForm(FlaskForm):
    address_name = StringField(
        'address_name',
        [DataRequired(), Regexp(r'^[a-zA-Z\s0-9]*$'), Length(min=4, max=25)]
    )
