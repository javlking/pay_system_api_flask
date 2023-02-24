from flask import Blueprint
from flask_restx import Api

# from . import cabinet, income_business, invoice_business

bp = Blueprint('business', __name__, url_prefix='/business')
api = Api(bp)

from . import cabinet, income_business, invoice_business

