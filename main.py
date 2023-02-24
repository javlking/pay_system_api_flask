from flask import Flask
from database.models import db

import business
import users

from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pay.db'
db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(users.bp)
# app.register_blueprint(users.card_service.bp, url_prefix='/card')
# app.register_blueprint(users.expenses_user.bp, url_prefix='/expenses')
# app.register_blueprint(users.registration.bp, url_prefix='/reg')
# app.register_blueprint(users.transfer_money.bp, url_prefix='/transfer')

app.register_blueprint(business.bp)
# app.register_blueprint(business.cabinet.bp, url_prefix='/cabinet')
# app.register_blueprint(business.income_business.bp, url_prefix='/income_track')
# app.register_blueprint(business.invoice_business.bp, url_prefix='/invoices')


@app.route('/')
def hello():
    return 'Salom'


# app.run()