from flask import Blueprint
from flask_restx import Api, Resource


bp = Blueprint('user-reg', __name__)
api = Api(bp)

model_user_register = api.parser()
model_user_register.add_argument('name', type=str, required=True)
model_user_register.add_argument('phone_number', type=str, required=True)


@api.route('/register')
class RegisterUser(Resource):
    @api.expect(model_user_register)
    def post(self):
        pass





