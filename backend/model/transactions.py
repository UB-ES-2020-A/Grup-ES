import datetime as dt
import json

from sqlalchemy import desc, func

from db import db
from utils.mail import send_email
from model.users import UsersModel
from model.books import BooksModel


class TransactionsModel(db.Model):
    __tablename__ = 'transactions'
    it_transaction = None

    id_transaction = db.Column(db.Integer(), primary_key=True)
    isbn = db.Column(db.BigInteger(), db.ForeignKey('books.isbn'), primary_key=True)
    price = db.Column(db.Float, nullable=False)
    id_user = db.Column(db.Integer(), db.ForeignKey('users.id'))
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    def __init__(self, isbn, id_user, quantity, date=None):

        if TransactionsModel.it_transaction is None:
            aux = TransactionsModel.query.order_by('id_transaction').first()
            TransactionsModel.it_transaction = 1 if aux is None else aux.id_transaction

        self.id_transaction = self.it_transaction
        self.isbn = isbn
        book = BooksModel.find_by_isbn(isbn)
        self.price = book.precio
        self.id_user = id_user
        self.quantity = quantity
        if date is None:
            self.date = dt.datetime.now()
        else:
            self.date = date

    def json(self):
        _ignore = self.isbn  # Forces execution to parse properly the class, fixing the bug of transient data
        atr = self.__dict__.copy()
        atr['isbn'] = BooksModel.find_by_isbn(self.isbn).isbn
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
    def save_transaction(cls, isbns, quantities, user_id):
        transactions = []
        for isbn, quantity in zip(isbns, quantities):
            transaction = TransactionsModel(isbn, user_id, quantity)
            transactions.append(transaction.json())
            book = BooksModel.find_by_isbn(isbn)
            if book.stock - quantity >= 0:
                book.stock -= quantity
            else:
                raise Exception('Not enough stock')
            db.session.add(transaction)

        cls.it_transaction += 1
        db.session.commit()
        recipient = UsersModel.find_by_id(user_id).email
        send_email(recipient, 'Order confirmation', json.dumps(transactions))
        return transactions
