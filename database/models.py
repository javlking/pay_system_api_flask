from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Модель пользователя
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_phone_number = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, nullable=False)
    reg_date = db.Column(db.DateTime, default=datetime.now())

    # Регистрация пользователя
    def register_user(self, phone_number, username):
        new_user = User(user_phone_number=phone_number, username=username)

        db.session.add(new_user)
        db.session.commit()

        return new_user.id

    # Изменить номер телефона
    def change_phone_number(self, user_id, new_phone_number):
        user = User.query.get_or_404(user_id)

        if user.user_phone_number != new_phone_number:
            user.user_phone_number = new_phone_number

            db.session.commit()
            return True

        else:
            return False


# Модель карт
class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, unique=True, autoincrement=True)
    card_number = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    amount = db.Column(db.Float)
    card_name = db.Column(db.String, default='Просто карта')
    exp_date = db.Column(db.Date, nullable=False)
    added_date = db.Column(db.DateTime, default=datetime.now())

    # Регистрация карты
    def register_card(self, user_id, card_number, exp_date, card_name):
        card = Card.query.get(card_number)

        if card:
            return 'Карта уже зарегистрирована'

        else:
            exp_date = datetime.strptime(exp_date, '%Y-%m-%d')
            new_card = Card(user_id=user_id, card_number=card_number, exp_date=exp_date, amount=0,
                            card_name=card_name)

            db.session.add(new_card)
            db.session.commit()

            return 'Карта зарегистрирована'

    # Удалить карту
    def delete_card(self, card_number):
        current_card = Card.query.get_or_404(card_number)

        if current_card:
            db.session.delete(current_card)
            db.session.commit()

            return True

        return False

    # Получение обьекта карты
    def get_card_object(self, card_id):
        current_card = Card.query.get(card_id)

        return current_card


# Модель платежей
class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    card_number = db.Column(db.Integer, db.ForeignKey('cards.card_number', ondelete='SET NULL'), nullable=False)
    amount = db.Column(db.Float)
    payment_type = db.Column(db.String, db.ForeignKey('services.service_type_name'))
    pay_date = db.Column(db.DateTime, default=datetime.now())

    card = db.relationship('Card')
    service_info = db.relationship('ServiceType')

    # Саздать платеж
    def create_payment(self, card_number, amount, service_type_name):
        card = Card().get_card_object(card_number)
        # Если на карте достаточно денег, то перевод
        if card.amount >= amount:
            new_payment = Payment(card_number=card.card_number,
                                  amount=amount,
                                  card=card,
                                  payment_type=service_type_name)

            db.session.add(new_payment)
            db.session.commit()

            return True

        return False

    # Мониторинг платежей
    def monitor_pays(self, card_number):
        card = Card().get_card_object(card_number)
        card_payments = Payment.query.filter_by(card_number=card.card_number).all()

        if card_payments:
            result = [{'pay_id': i.id,
                       'pay_type': i.payment_type,
                       'amount': i.amount,
                       'date': str(i.pay_date)}
                      for i in card_payments]

            return result

        return False


# Модель бизнеса
class Business(db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), primary_key=True)
    service_name = db.Column(db.String(55))
    business_card = db.Column(db.Integer, db.ForeignKey('cards.card_number', ondelete='SET NULL'))
    service_type = db.Column(db.String, db.ForeignKey('services.service_type_name'))
    opened = db.Column(db.DateTime, default=datetime.now())

    card_data = db.relationship(Card)

    # Регистрация бизнеса
    def register_business(self, user_id, service_name, service_type, which_card):
        checker = Card.query.get(which_card)

        if checker and checker.user_id == user_id:
            new_business = Business(user_id=user_id, service_name=service_name,
                                    business_card=which_card, card_data=checker,
                                    service_type=service_type)

            db.session.add(new_business)
            db.session.commit()

            return True

        return False


# Модель типа сервиса
class ServiceType(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    service_category = db.Column(db.String)
    service_type_name = db.Column(db.String, unique=True)
    opened = db.Column(db.DateTime, default=datetime.now())

    # Регистрация типа сервиса
    def register_service_type(self, service_name, service_type_name):
        new_service_type = ServiceType(service_category=service_name,
                                       service_type_name=service_type_name)

        db.session.add(new_service_type)
        db.session.commit()

        return True


# Денежные переводы между пользователями
class TransfersP2P(db.Model):
    __tablename__ = 'p2p'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_from_card = db.Column(db.Integer, db.ForeignKey('cards.card_number', ondelete='SET NULL'))
    user_to_card = db.Column(db.Integer)
    amount = db.Column(db.Float)
    p2p_date = db.Column(db.DateTime, default=datetime.now())

    card_data = db.relationship(Card)

    # Зафиксировать перевод
    def create_payment(self, user_id, user_from_card, user_to_card, amount):
        from_card = Card().get_card_object(user_from_card)
        to_card = Card().get_card_object(user_to_card)

        # Если на карте достаточно денег, то перевод
        if from_card.amount >= amount:
            new_payment = TransfersP2P(user_id=user_id, user_from_card=user_from_card,
                                       user_to_card=user_to_card, amount=amount)

            db.session.add(new_payment)

            from_card.amount -= amount
            to_card.amount += amount

            db.session.commit()

            return 'Успешно'

        return 'Недостаточно средств'

