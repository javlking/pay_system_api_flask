from flask import Blueprint

from flask_restx import Api
# from . import card_service, expenses_user, registration, transfer_money

bp = Blueprint('users', __name__, url_prefix='/users')
api = Api(bp)

from . import card_service, expenses_user, registration, transfer_money

