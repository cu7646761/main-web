from functools import wraps
from flask import redirect, render_template, Blueprint, session, request

from app.main.comment.forms import CommentForm
from app.main.comment.models import CommentModel

from utils import Utils

comment_blueprint = Blueprint(
    'comment', __name__, template_folder='templates')

