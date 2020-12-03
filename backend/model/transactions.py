import datetime as dt
import json
from sqlalchemy import desc

from db import db

from utils.mail import send_email

from model.library import LibraryModel, LibraryType, State
from model.users import UsersModel
from model.books import BooksModel


class TransactionsModel(db.Model):
    __tablename__ = 'transactions'
    it_transaction = None

    id_transaction = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    isbn = db.Column(db.BigInteger(), db.ForeignKey('books.isbn'), primary_key=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    def __init__(self, user_id, isbn, price, quantity, date=None):

        if TransactionsModel.it_transaction is None:
            aux = TransactionsModel.query.order_by(desc('id_transaction')).first()
            TransactionsModel.it_transaction = 1 if aux is None else aux.id_transaction + 1

        self.id_transaction = self.it_transaction
        self.isbn = isbn
        self.price = price
        self.user_id = user_id

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
        atr['book'] = BooksModel.find_by_isbn(atr['isbn']).json()
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

    def send_confirmation_mail(self):
        recipient = UsersModel.find_by_id(self.user_id).email
        quantity = str(self.quantity)
        isbn = str(self.isbn)
        subject = 'Order confirmation'
        message = 'Has comprat ' + quantity + ' llibre/s amb isbn ' + isbn
        send_email(recipient, subject, message)

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
            book = BooksModel.find_by_isbn(isbn)
            cls.check_stock(book, quantity)
            transaction = TransactionsModel(user_id, isbn, price, quantity)
            transactions.append(transaction.json())
            db.session.add(transaction)
            user = UsersModel.find_by_id(user_id)
            if LibraryModel.find_by_id_and_isbn(user.id, transaction.isbn) is None:
                entry = LibraryModel(book.isbn, user.id, LibraryType.Bought, State.Pending)
                db.session.add(entry)

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

    @classmethod
    def best_sellers(cls):
        aux = {}
        for transaction in cls.query.all():
            isbn = transaction.isbn
            quantity = transaction.quantity
            aux[isbn] = quantity + aux.get(isbn, 0)
        sort_best = dict(sorted(aux.items(), key=lambda x: x[1], reverse=True))
        isbns = list(sort_best.keys())
        return isbns

    @classmethod
    def group_transactions_by_id(cls, transactions):
        grouped_transactions = [[t.json() for t in transactions if t.id_transaction == i] for i in
                                set(t.id_transaction for t in transactions)]
        return grouped_transactions
