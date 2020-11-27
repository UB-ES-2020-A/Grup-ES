import datetime as dt
import json

from db import db
from utils.mail import send_email
from model.users import UsersModel
from model.books import BooksModel


class TransactionsModel(db.Model):
    __tablename__ = 'transactions'
    it_transaction = None

    id_transaction = db.Column(db.Integer(), primary_key=True)
    id_user = db.Column(db.Integer(), db.ForeignKey('users.id'))
    isbn = db.Column(db.BigInteger(), db.ForeignKey('books.isbn'), primary_key=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    def __init__(self, id_user, isbn, price, quantity, date=None):

        if TransactionsModel.it_transaction is None:
            aux = TransactionsModel.query.order_by('id_transaction').first()
            TransactionsModel.it_transaction = 1 if aux is None else aux.id_transaction

        self.id_transaction = self.it_transaction
        self.isbn = isbn
        self.price = price
        self.id_user = id_user
        self.quantity = quantity
        if date is None:
            self.date = dt.datetime.now()
        else:
            self.date = date

    def json(self):
        _ignore = self.isbn  # Forces execution to parse properly the class, fixing the bug of transient data
        atr = self.__dict__.copy()
        del atr["_sa_instance_state"]
        atr['date'] = self.date.strftime('%d-%m-%Y')
        return atr

    def save_to_db(self):
        db.session.add(self)
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

    @classmethod
    def find_by_id(cls, id_transaction):
        return cls.query.filter_by(id_transaction=id_transaction).all()

    @classmethod
    def find_by_id_and_isbn(cls, id_transaction, isbn):
        return cls.query.filter_by(id_transaction=id_transaction, isbn=isbn).first()

    @classmethod
    def save_transaction(cls, user_id, isbns, prices, quantities):
        transactions = []
        for isbn, price, quantity in zip(isbns, prices, quantities):
            transaction = TransactionsModel(user_id, isbn, price, quantity)
            transactions.append(transaction.json())
            book = BooksModel.find_by_isbn(isbn)
            cls.check_stock(book, quantity)
            db.session.add(transaction)

        cls.it_transaction += 1
        db.session.commit()
        recipient = UsersModel.find_by_id(user_id).email
        send_email(recipient, 'Order confirmation', json.dumps(transactions))
        return transactions

    @classmethod
    def check_stock(cls, book, quantity):
        if book.stock - quantity >= 0:
            book.stock -= quantity
        else:
            raise Exception('Not enough stock')
