from flask import g
from flask_restful import reqparse
from flask_restful import Resource

from model.users import auth, UsersModel
from model.transactions import TransactionsModel
from utils.lock import lock


def parse_transaction(minimal=False):
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('isbn', type=int, required=not minimal,
                        help="In this field goes the isbn of the book, cannot be left blank")
    parser.add_argument('price', type=float, required=not minimal,
                        help="In this field goes the price of the book, cannot be left blank")
    parser.add_argument('email', type=str, required=not minimal,
                        help="In this field goes the email of the user, cannot be left blank")
    parser.add_argument('quantity', type=str, required=not minimal,
                        help="In this field goes the quantity of books")

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
            data['user_id'] = user.id
            del data['email']
            try:
                transaction = TransactionsModel(**data)
                transaction.save_to_db()
            except Exception as e:
                return {"message": str(e)}, 500
        return transaction.json(), 201


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
        return {'transactions': [transaction.json() for transaction in transactions]}, 200
