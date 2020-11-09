import unittest

from tests.base_test import BaseTest
from model.transactions import TransactionsModel


class UnitTestOfUS(BaseTest):

    # TEST TASK 1
    def test_model_add(self):
        with self.app.app_context():
            entry = TransactionsModel(1, 2.2, 1, True, None)
            entry.save_to_db()
            self.assertEqual(entry, TransactionsModel.find_by_id_and_isbn(1, 1))

    """
    #Not necessary
    def test_model_add_duplicate(self):
        with self.app.app_context():
            entry = TransactionsModel(1, 2.2, 1, True, None)
            entry.save_to_db()

            same_entry = entry = TransactionsModel(1, 2.2, 1, True, None)
            with self.assertRaises(Exception):
                same_entry.save_to_db()
    """

    def test_model_delete(self):
        with self.app.app_context():
            entry = TransactionsModel(1, 2.2, 1, True, None)
            entry.save_to_db()
            entry.delete_from_db()

            self.assertEqual(TransactionsModel.find_by_id_and_isbn(1, 1), None)

    def test_model_update(self):
        with self.app.app_context():
            entry = TransactionsModel(1, 2.2, 1, True, None)  # isbn = 1
            entry.save_to_db()

            data = {"isbn": 2}  # isbn = 2
            entry.update_from_db(data)

            self.assertEqual(entry.json(), TransactionsModel.find_by_id_and_isbn(1, 2).json())  # isbn = 2

    def test_model_invalid_update(self):
        with self.app.app_context():
            entry = TransactionsModel(1, 2.2, 1, True, None)
            entry.save_to_db()

            with self.assertRaises(Exception):
                data = {"isbn": "patata"}  # has to be integer
                entry.update_from_db(data)

    def test_model_invalid_update2(self):
        with self.app.app_context():
            entry = TransactionsModel(1, 2.2, 1, True, None)
            entry.save_to_db()

            with self.assertRaises(Exception):
                data = {"price": 10}  # has to be a float
                entry.update_from_db(data)


if __name__ == '__main__':
    unittest.main()
