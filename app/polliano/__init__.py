from flask import Blueprint

polliano_blueprint = Blueprint('polliano', __name__)

from . import views
