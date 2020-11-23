import base64
import unittest
import json

from model.books import BooksModel
from model.users import UsersModel
from tests.base_test import BaseTest
from model.transactions import TransactionsModel
import datetime as dt


class UnitTestOfUS(BaseTest):

    # TEST TASK 1
    def test_model_add(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'bookshelterES@gmail.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)
            id_user = UsersModel.find_by_email(to_add.email).id

            book = BooksModel(1, 1, 1, "book1")
            book.save_to_db()
            book2 = BooksModel(2, 1, 1, "book2")
            book2.save_to_db()

            TransactionsModel.save_transaction([book.isbn], [1], id_user)
            TransactionsModel.save_transaction([book2.isbn], [6], id_user)
            self.assertEqual(1, len(TransactionsModel.find_by_id(1)))
            self.assertEqual(1, len(TransactionsModel.find_by_id(2)))

    def test_model_delete(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'bookshelterES@gmail.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)
            id_user = UsersModel.find_by_email(to_add.email).id

            book = BooksModel(1, 1, 1, "book1")
            book.save_to_db()

            TransactionsModel.save_transaction([book.isbn], [1], id_user)
            self.assertEqual(1, len(TransactionsModel.query.all()))

            TransactionsModel.query.filter_by(id_transaction=1).first().delete_from_db()
            self.assertEqual(0, len(TransactionsModel.query.all()))

    def test_model_update(self):
        with self.app.app_context():
            user = UsersModel('test', 'bookshelterES@gmail.com')
            user.hash_password('password')
            user.save_to_db()

            book = BooksModel(1, 1, 1, "titulo")
            book.save_to_db()

            TransactionsModel.save_transaction([book.isbn], [1], user.id)
            self.assertEqual(1, len(TransactionsModel.query.all()))

            data = {"id_transaction": 10}  # id = 10
            TransactionsModel.query.filter_by(id_transaction=1).first().update_from_db(data)
            expected_output = {'date': dt.datetime.today().strftime("%d-%m-%Y"),
                               'id_transaction': 10,
                               'id_user': 1,
                               'isbn': 1,
                               'price': 1.0,
                               'quantity': 1}

            self.assertEqual(expected_output, TransactionsModel.find_by_id(data["id_transaction"])[0].json())

    def test_model_invalid_update(self):
        with self.app.app_context():
            user = UsersModel('test', 'bookshelterES@gmail.com')
            user.hash_password('password')
            user.save_to_db()

            book = BooksModel(1, 1, 1, "titulo")
            book.save_to_db()

            TransactionsModel.save_transaction([book.isbn], [1], user.id)
            self.assertEqual(1, len(TransactionsModel.query.all()))

            data = {"id_transaction": 'string'}  # must be an integer
            with self.assertRaises(Exception):
                TransactionsModel.query.filter_by(id_transaction=1).first().update_from_db(data)

    # TEST TASK 2
    def test_post(self):
        with self.app.app_context():
            user = UsersModel('test', 'bookshelterES@gmail.com')
            user.hash_password('test')
            UsersModel.save_to_db(user)

            book = BooksModel(1, 1, 1.0, "book1")
            book.save_to_db()
            book = BooksModel(2, 2, 13.1, "book2")
            book.save_to_db()

            isbns = [1, 2]
            quantities = [1, 1]
            dataTransaction = {
                "isbns": isbns,
                'quantities': quantities,
                "email": user.email,
            }
            res = self.client.post("/login", data={"email": user.email, "password": "test"})
            token = json.loads(res.data)["token"]

            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            self.assertEqual("ISBNs of books in transaction with id = 1 are [1, 2]",
                             TransactionsModel.find_isbns_by_id(1))

    # TEST TASK 3
    # test manual: posar variable config TESTING = False i veure com es reb el mail correctament.
    def test_order_mail(self):
        with self.app.app_context():
            user = UsersModel('test', 'bookshelterES@gmail.com')
            user.hash_password('test')
            UsersModel.save_to_db(user)

            book = BooksModel(1, 1, 1.0, "book1")
            book.save_to_db()
            book = BooksModel(2, 2, 13.1, "book2")
            book.save_to_db()

            isbns = [1, 2]
            quantities = [1, 1]
            dataTransaction = {
                "isbns": isbns,
                'quantities': quantities,
                "email": user.email,
            }
            res = self.client.post("/login", data={"email": user.email, "password": "test"})
            token = json.loads(res.data)["token"]

            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            self.assertEqual("ISBNs of books in transaction with id = 1 are [1, 2]",
                             TransactionsModel.find_isbns_by_id(1))

    # TEST TASK 6
    def test_get_transactions_user(self):
        with self.app.app_context():
            user = UsersModel('test', 'bookshelterES@gmail.com')
            user.hash_password('test')
            UsersModel.save_to_db(user)

            book = BooksModel(1, 1, 1.0, "book1")
            book.save_to_db()
            book = BooksModel(2, 2, 13.1, "book2")
            book.save_to_db()

            isbns = [1, 2]
            quantities = [1, 1]
            dataTransaction = {
                "isbns": isbns,
                'quantities': quantities,
                "email": user.email,
            }
            res = self.client.post("/login", data={"email": user.email, "password": "test"})
            token = json.loads(res.data)["token"]

            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            self.assertEqual("ISBNs of books in transaction with id = 1 are [1, 2]",
                             TransactionsModel.find_isbns_by_id(1))

    def test_get_transactions_without_login(self):
        with self.app.app_context():
            user = UsersModel('test', 'bookshelterES@gmail.com')
            user.hash_password('test')
            UsersModel.save_to_db(user)

            book = BooksModel(1, 1, 1.0, "titulo")
            book.save_to_db()

            dataTransaction = {
            }

            res = self.client.post("/transaction", data=dataTransaction)
            self.assertEqual(401, res.status_code)

    def test_get_transactions_other_user(self):
        with self.app.app_context():
            user = UsersModel('test', 'bookshelterES@gmail.com')
            user.hash_password('test')
            UsersModel.save_to_db(user)

            book = BooksModel(1, 1, 1.0, "book1")
            book.save_to_db()
            book = BooksModel(2, 2, 13.1, "book2")
            book.save_to_db()

            isbns = [1, 2]
            quantities = [1, 1]
            dataTransaction = {
                "isbns": isbns,
                'quantities': quantities,
                "email": user.email,
            }
            res = self.client.post("/login", data={"email": user.email, "password": "test"})
            token = json.loads(res.data)["token"]

            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            user2 = UsersModel('test2', 'patata@gmail.com')
            user2.hash_password('test2')
            UsersModel.save_to_db(user2)

            res = self.client.get('/transactions/' + user2.email, headers={  # user tries to get user2 transactions
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(401, res.status_code)


if __name__ == '__main__':
    unittest.main()
