from functools import wraps
from flask import redirect, render_template, Blueprint, session, request

from app.main.category.forms import CategoryForm
from app.main.category.models import CategoryModel

from utils import Utils

category_blueprint = Blueprint(
    'category', __name__, template_folder='templates')

