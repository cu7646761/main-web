from functools import wraps
from flask import redirect, render_template, Blueprint, session, request

from app.main.address.forms import AddressForm
from app.main.address.models import AddressModel

from utils import Utils

address_blueprint = Blueprint(
    'address', __name__, template_folder='templates')

