from flask import Blueprint
from flask_restx import Api, Resource

bp = Blueprint('income_business', __name__)
api = Api(bp)

income_model = api.parser()
income_model.add_argument('user_id', type=int, required=True)


@api.route('/income')
class GetBusinessIncome(Resource):
    @api.expect(income_model)
    def get(self):
        pass





