from flask import Blueprint

comment_blueprint = Blueprint(
    'comment', __name__, template_folder='templates')

