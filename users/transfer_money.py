from flask import Blueprint
from flask_restx import Api, Resource

from database.models import TransfersP2P

import random

# bp = Blueprint('transfer-money', __name__)
# api = Api(bp)
from users import api

model_transfer_money = api.parser()
model_transfer_money.add_argument('user_from_id', type=int, required=True)
model_transfer_money.add_argument('user_from_card', type=int, required=True)
model_transfer_money.add_argument('to_card', type=int, required=True)
model_transfer_money.add_argument('amount', type=float, required=True)
model_transfer_money.add_argument('verify_code', type=int, required=True)


model_pay_service = api.parser()
model_pay_service.add_argument('service_id', type=int, required=True)
model_pay_service.add_argument('amount', type=float, required=True)
model_pay_service.add_argument('from_card', type=int, required=True)


model_verify = api.parser()
model_verify.add_argument('card_number', type=int, required=True)


test_ver = {}


# Transfer money to other user
@api.route('/transfer-money')
class TransferMoney(Resource):
    @api.expect(model_transfer_money)
    def post(self):
        args = model_transfer_money.parse_args()

        user_from_id = args.get('user_from_id')
        user_from_card = args.get('user_from_card')
        to_card = args.get('to_card')
        amount = args.get('amount')
        code = args.get('verify_code')

        if test_ver[user_from_card] == code:
            result = TransfersP2P().create_payment(user_from_id, user_from_card, to_card, amount)

            return {'status': 1, 'message': result}

        return {'status': 0, 'message': 'За тобой уже выехали'}


# Pay for some service
@api.route('/pay-service')
class PayService(Resource):
    @api.expect(model_pay_service)
    def post(self):
        return ''


# Get verification code
@api.route('/get-verify-code')
class GetVerify(Resource):
    @api.expect(model_verify)
    def get(self):
        args = model_verify.parse_args()
        card_number = args.get('card_number')

        verify_code = random.randint(1212, 9999)

        test_ver[card_number] = verify_code

        return {'status': 1, 'code': verify_code}


