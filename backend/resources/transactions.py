from flask import g
from flask_restful import reqparse
from flask_restful import Resource
from sqlalchemy import asc, desc

from model.books import BooksModel
from model.users import auth, UsersModel
from model.transactions import TransactionsModel
from utils.lock import lock


def parse_transaction():
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('email', type=str,
                        help="In this field goes the email of the user, cannot be left blank")
    parser.add_argument('isbns', type=int, action='append',
                        help="In this field goes the isbns of the books, cannot be left blank")
    parser.add_argument('prices', type=float, action='append',
                        help="In this field goes the prices of the books, cannot be left blank")
    parser.add_argument('quantities', type=int, action='append',
                        help="In this field goes the quantity of each book, cannot be left blank")
    return parser.parse_args()


class Transactions(Resource):
    @auth.login_required
    def get(self, id_transaction):
        with lock:
            transaction = TransactionsModel.find_by_id(id_transaction)
            if not transaction:
                return {"message": f"Transaction with ['id_transaction':{id_transaction}] not found"}, 404
            if UsersModel.find_by_id(transaction.user_id) != g.user:
                return {"message": "Invalid transaction, can only be yours"}, 401
        return {"transaction": transaction.json()}, 200

    @auth.login_required
    def post(self):
        data = parse_transaction()
        with lock:
            user = UsersModel.find_by_email(data['email'])
            if user is None:
                return {"message": f"User with ['email': {data['email']}] Not Found"}, 404
            if user != g.user:
                return {"message": "Invalid transaction, can only post yours"}, 401
            for isbn, quantity in zip(data['isbns'], data['quantities']):
                book = BooksModel.find_by_isbn(isbn)
                if book is None:
                    return {"message": "Book with ['isbn': " + str(isbn) + "] Not Found"}, 404
                if quantity > book.stock:
                    return {"message": "Not enough stock for book with 'isbn': " + str(isbn) + "only "
                                       + str(book.stock) + " available"}, 404
            try:
                transactions = TransactionsModel.save_transaction(user.id, data['isbns'], data['prices'],
                                                                  data['quantities'])
            except Exception as ex:
                return {'message': str(ex)}, 500
        return {'transactions': transactions}, 201


class TransactionsUser(Resource):
    @auth.login_required
    def get(self, email):
        with lock:
            user = UsersModel.find_by_email(email)
            if user is None:
                return {"message": "User with ['email': " + email + "] Not Found"}, 404
            if g.user != user:
                return {"message": "Invalid user, can only be yourself"}, 401
            transactions = TransactionsModel.query.filter_by(user_id=user.id).all()
            grouped_transactions = TransactionsModel.group_transactions_by_id(transactions)
            return {'transactions': grouped_transactions}, 200


class TransactionsList(Resource):
    @auth.login_required(role='Admin')
    def get(self):
        with lock:
            parser = reqparse.RequestParser(bundle_errors=True)

            parser.add_argument('isbn', type=int, required=False,
                                help="In this field goes the isbn of the transactions")
            # parser.add_argument('titulo', type=str, required=False,
            # help="In this field goes the tittle of the book")
            parser.add_argument('user_id', type=int, required=False,
                                help="In this field goes the user_id of the transactions")
            parser.add_argument('date', type=str, required=False,
                                help="In this field goes the date order (asc, desc) of the transactions")
            data = parser.parse_args()

            transactions = TransactionsModel.query
            if not any(v is not None for k, v in data.items()):  # no filter asked
                grouped_transactions = TransactionsModel.group_transactions_by_id(transactions)
                return {'transactions': grouped_transactions}, 200
            else:
                for k, v in data.items():
                    if v is not None:
                        if k != 'date':
                            transactions = transactions.filter(getattr(TransactionsModel, k) == v)

            if data['date'] == 'asc':
                transactions = transactions.order_by(asc('date'))
            elif data['date'] == 'desc':
                transactions = transactions.order_by(desc('date'))

            grouped_transactions = TransactionsModel.group_transactions_by_id(transactions)
            return {'transactions': grouped_transactions}, 200
