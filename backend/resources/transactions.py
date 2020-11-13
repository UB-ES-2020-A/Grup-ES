from flask_restful import reqparse
from flask_restful import Resource
from model.users import auth, UsersModel

from model.transactions import TransactionsModel


def parse_transaction(minimal=False):
    str_variable = ", cannot be left blank"
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('isbn', type=int, required=not minimal,
                        help="In this field goes the isbn of the book" + str_variable)
    parser.add_argument('price', type=float, required=not minimal,
                        help="In this field goes the price of the book" + str_variable)
    parser.add_argument('id_user', type=str, required=not minimal,
                        help="In this field goes the id of the user" + str_variable)
    parser.add_argument('quantity', type=str, required=not minimal,
                        help="In this field goes the quantity of books")

    data = parser.parse_args()

    return data


class Transactions(Resource):
    @auth.login_required()
    def get(self, id):
        transaction = TransactionsModel.find_by_id(id)
        if not transaction:
            return {"message": f"Transaction with ['id_transaction':{id}] not found"}, 404
        return {"book": transaction.json()}, 200

    @auth.login_required()
    def post(self):
        data = parse_transaction()
        try:
            transaction = TransactionsModel(**data)
            transaction.save_to_db()
        except Exception as e:
            return {"message": str(e)}, 500
        return transaction.json(), 201


class TransactionsUser(Resource):
    @auth.login_required()
    def get(self, id_user):
        user = UsersModel.find_by_id(id_user)
        if user is None:
            return {"message": "User with ['id_user': " + str(id_user) + "] Not Found"}, 404
        transactions = TransactionsModel.query.filter_by(id_user=id_user).all()
        if len(transactions) == 0:
            return {}
        return {'transactions': [transaction.json() for transaction in transactions]}, 200
