import datetime as dt

from db import db
from utils.mail import send_email
from model.users import UsersModel
from model.books import BooksModel


class TransactionsModel(db.Model):
    __tablename__ = 'transactions'
    __id_transaction = 0

    id_transaction = db.Column(db.Integer(), primary_key=True)
    isbn = db.Column(db.BigInteger(), primary_key=True)
    price = db.Column(db.Float, nullable=False)
    id_user = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    def __init__(self, isbn, price, id_user, quantity, date=None):
        self.id_transaction = self.__id_transaction
        self.isbn = isbn
        self.price = float(price)
        self.id_user = id_user
        self.quantity = quantity
        if date is None:
            self.date = dt.datetime.now()
        else:
            self.date = date

    def json(self):
        _ignore = self.isbn  # Forces execution to parse properly the class, fixing the bug of transient data
        atr = self.__dict__.copy()
        atr['book'] = BooksModel.find_by_isbn(self.isbn).json()
        del atr['isbn']
        del atr["_sa_instance_state"]
        atr['date'] = self.date.strftime('%d-%m-%Y')
        return atr

    def save_to_db(self):
        db.session.add(self)
        self.send_confirmation_mail()
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_from_db(self, data):
        for attr, newValue in data.items():
            if newValue is not None:
                cls = getattr(self, attr)
                if isinstance(newValue, type(cls)):
                    setattr(self, attr, newValue)
                else:
                    raise Exception
        db.session.commit()

    def send_confirmation_mail(self):
        recipient = UsersModel.find_by_id(self.id_user).email
        quantity = str(self.quantity)
        isbn = str(self.isbn)
        subject = 'Order confirmation'
        message = 'Has comprat ' + quantity + ' llibre/s amb isbn ' + isbn
        send_email(recipient, subject, message)

    @classmethod
    def find_by_id(cls, id_transaction):
        return cls.query.filter_by(id_transaction=id_transaction).all()


