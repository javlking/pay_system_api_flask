from flask import Blueprint
from flask_restx import Api, Resource

from database.models import User

# bp = Blueprint('user-reg', __name__)
# api = Api(bp)
from users import api
model_user_register = api.parser()
model_user_register.add_argument('name', type=str, required=True)
model_user_register.add_argument('phone_number', type=str, required=True)


@api.route('/register')
class RegisterUser(Resource):
    @api.expect(model_user_register)
    def post(self):
        user_data = model_user_register.parse_args()

        user_number = user_data.get('phone_number')
        username = user_data.get('name')

        user_id = User().register_user(user_number, username)

        return {'status': 1, 'user_id': user_id}






