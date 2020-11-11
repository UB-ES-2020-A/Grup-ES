import unittest
import json

from flask_mail import Mail

from tests.base_test import BaseTest
from model.transactions import TransactionsModel


class UnitTestOfUS(BaseTest):

    # TEST TASK 1
    def test_model_add(self):
        with self.app.app_context():
            entry = TransactionsModel(1, 2.2, 1, 1, None)
            entry.save_to_db()
            self.assertEqual(entry, TransactionsModel.find_by_id(1))

    def test_model_delete(self):
        with self.app.app_context():
            entry = TransactionsModel(1, 2.2, 1, 1, None)
            entry.save_to_db()
            entry.delete_from_db()

            self.assertEqual(TransactionsModel.find_by_id(1), None)

    def test_model_update(self):
        with self.app.app_context():
            entry = TransactionsModel(1, 2, 1, 1, None)  # id_transaction = 1 -> es automatica
            entry.save_to_db()

            data = {"id_transaction": 10}  # id = 10
            entry.update_from_db(data)
            self.assertEqual(entry.json(), TransactionsModel.find_by_id(10).json())

    def test_model_invalid_update(self):
        with self.app.app_context():
            entry = TransactionsModel(1, 2.2, 1, 1, None)
            entry.save_to_db()

            with self.assertRaises(Exception):
                data = {"isbn": "patata"}  # has to be integer
                entry.update_from_db(data)

    # TEST TASK 2
    def test_post(self):
        with self.app.app_context():
            data = {
                "isbn": 1,
                "price": 7.9,
                "id_user": 1,
                "quantity": 1
            }
            res = self.client.post("/transaction", data=data)
            self.assertEqual(201, res.status_code)
            self.assertEqual(json.loads(res.data), TransactionsModel.query.first().json())  # json.loads(res.data))

    # TEST TASK 3
    def test_order_mail(self):
        with self.app.app_context():
            data = {
                "isbn": 5,
                "price": 7.9,
                "id_user": 1,
                "quantity": 1
            }
            res = self.client.post("/transaction", data=data)
            self.assertEqual(201, res.status_code)
            self.assertEqual(json.loads(res.data), TransactionsModel.query.first().json())
            #outbox len?


if __name__ == '__main__':
    unittest.main()
