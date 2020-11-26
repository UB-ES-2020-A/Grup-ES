from flask import g
from flask_restful import reqparse
from flask_restful import Resource

from model.books import BooksModel
from model.users import auth, UsersModel
from model.transactions import TransactionsModel


def parse_transaction():
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('email', type=str,
                        help="In this field goes the email of the user, cannot be left blank")
    parser.add_argument('isbns', type=int, action='append',
                        help="In this field goes the isbns of the books, cannot be left blank")
    parser.add_argument('quantities', type=int, action='append',
                        help="In this field goes the quantity of each book, cannot be left blank")
    return parser.parse_args()


class Transactions(Resource):
    @auth.login_required
    def get(self, id):
        transaction = TransactionsModel.find_by_id(id)
        if not transaction:
            return {"message": f"Transaction with ['id_transaction':{id}] not found"}, 404
        if UsersModel.find_by_id(transaction.user_id) != g.user:
            return {"message": "Invalid transaction, can only be yours"}, 401
        return {"transaction": transaction.json()}, 200

    @auth.login_required
    def post(self):
        data = parse_transaction()
        dataTransaction = {}
        user = UsersModel.find_by_email(data['email'])
        if user is None:
            return {"message": "User with ['id_user': " + str(user.id_user) + "] Not Found"}, 404
        if user != g.user:
            return {"message": "Invalid transaction, can only post yours"}, 401
        for isbn in data['isbns']:
            book = BooksModel.find_by_isbn(isbn)
            if book is None:
                return {"message": "Book with ['isbn': " + str(isbn) + "] Not Found"}, 404
        try:
            transactions = TransactionsModel.save_transaction(data['isbns'], data['quantities'], user.id)
        except Exception as ex:
            return {'message': str(ex)}, 500
        return {'transactions': transactions}, 201


class TransactionsUser(Resource):
    @auth.login_required
    def get(self, email):
        user = UsersModel.find_by_email(email)
        if user is None:
            return {"message": "User with ['email': " + email + "] Not Found"}, 404
        if g.user != user:
            return {"message": "Invalid user, can only be yourself"}, 401
        return {'transactions': [transaction.json() for transaction in user.transactions]}, 200
