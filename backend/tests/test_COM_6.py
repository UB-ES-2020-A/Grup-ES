import unittest

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


if __name__ == '__main__':
    unittest.main()
