from flask import Blueprint
from flask_restx import Api, Resource

from database.models import Business

# bp = Blueprint('cabinet', __name__)
# api = Api(bp)

from business import api

model_service_register = api.parser()
model_service_register.add_argument('user_id', type=int, required=True)
model_service_register.add_argument('service_name', type=str, required=True)
model_service_register.add_argument('service_type', type=str, required=True)
model_service_register.add_argument('which_card', type=int, required=True)


@api.route('/add-service')
class AddService(Resource):
    @api.expect(model_service_register)
    def post(self):
        args = model_service_register.parse_args()

        user_id = args.get('user_id')
        service_name = args.get('service_name')
        service_type = args.get('service_type')
        which_card = args.get('which_card')

        message = Business().register_business(user_id, service_name, service_type, which_card)

        return {'status': 1, 'message': str(message)}








