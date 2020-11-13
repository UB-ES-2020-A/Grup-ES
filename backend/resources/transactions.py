from flask_restful import reqparse
from flask_restful import Resource

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

    def get(self, id):
        transaction = TransactionsModel.find_by_id(id)
        if not transaction:
            return {"message": f"Transaction with ['id_transaction':{id}] not found"}, 404
        return {"book": transaction.json()}, 200

    def post(self):
        data = parse_transaction()
        try:
            transaction = TransactionsModel(**data)
            transaction.save_to_db()
        except Exception as e:
            return {"message": str(e)}, 500

        return transaction.json(), 201
