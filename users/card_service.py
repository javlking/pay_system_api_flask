from flask import Blueprint
from flask_restx import Api, Resource

from database.models import Card

# bp = Blueprint('card_service', __name__)
# api = Api(bp)

from users import api

model_card_add = api.parser()
model_card_add.add_argument('user_id', type=int, required=True)
model_card_add.add_argument('card_number', type=int, required=True)
model_card_add.add_argument('exp_date', type=str, required=True)
model_card_add.add_argument('card_name', type=str, required=False)
model_card_add.add_argument('phone_number', type=str, required=True)


model_card_delete = api.parser()
model_card_delete.add_argument('card_number', type=int, required=True)


# Add card
@api.route('/add-card')
class AddCardUser(Resource):
    @api.expect(model_card_add)
    def post(self):
        card_data = model_card_add.parse_args()

        user_id = card_data.get('user_id')
        card_number = card_data.get('card_number')
        exp_date = card_data.get('exp_date')
        card_name = card_data.get('card_name')
        phone_number = card_data.get('phone_number')

        new_card = Card().register_card(user_id, card_number, exp_date, card_name)

        return {'status': 1, 'message': new_card}


# Delete card
@api.route('/delete-card')
class DeleteCard(Resource):
    @api.expect(model_card_delete)
    def delete(self):
        card_data = model_card_delete.parse_args()

        card_number = card_data.get('card_number')
        deleter = Card().delete_card(card_number)

        if deleter:
            return {'status': 1, 'message': 'Deleted'}

        return {'status': 0, 'message': 'Ошибка в данных'}





