from flask import Blueprint
from flask_restx import Api, Resource

from database.models import TransfersP2P

# bp = Blueprint('expenses', __name__)
# api = Api(bp)
from users import api

model_get_expenses = api.parser()
model_get_expenses.add_argument('card_number', type=int, required=False)


# Get user expenses
@api.route('/user-expenses')
class GetUserExpenses(Resource):
    @api.expect(model_get_expenses)
    def get(self):
        card_number = model_get_expenses.parse_args()

        result = TransfersP2P().monitoring_pays(card_number.get('card_number'))

        if result:
            return {'status': 1, 'message': result}

        return {'status': 0, 'message': 'Ничего не нашел'}





