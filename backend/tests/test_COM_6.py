import base64
import unittest
import json

from model.books import BooksModel
from model.users import UsersModel
from tests.base_test import BaseTest
from model.transactions import TransactionsModel
import datetime as dt


class UnitTestOfUS(BaseTest):

    def tearDown(self):
        super().tearDown()
        with self.app.app_context():
            TransactionsModel.it_transaction = 1

    def basic_setup(self):
        self.user = UsersModel("test", "bookshelterES@gmail.com")
        self.user.hash_password("test")
        self.user.save_to_db()

        self.book = BooksModel(1, 1, 1, "book1")
        self.book.save_to_db()

        res = self.client.post("/login", data={"email": self.user.email, "password": "test"})
        self.token = json.loads(res.data)["token"]

    # TEST TASK 1
    def test_model_add(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 1, 1, "book2")
            book2.save_to_db()

            TransactionsModel.save_transaction([self.book.isbn], [1], self.user.id)
            self.assertEqual(1, len(TransactionsModel.find_by_id(1)))
            TransactionsModel.save_transaction([book2.isbn], [1], self.user.id)
            self.assertEqual(1, len(TransactionsModel.find_by_id(2)))

    def test_model_delete(self):
        with self.app.app_context():
            self.basic_setup()

            TransactionsModel.save_transaction([self.book.isbn], [1], self.user.id)
            self.assertEqual(1, len(TransactionsModel.query.all()))

            TransactionsModel.query.filter_by(id_transaction=1).first().delete_from_db()
            self.assertEqual(0, len(TransactionsModel.query.all()))

    def test_model_update(self):
        with self.app.app_context():
            self.basic_setup()

            TransactionsModel.save_transaction([self.book.isbn], [1], self.user.id)
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
            self.basic_setup()

            TransactionsModel.save_transaction([self.book.isbn], [1], self.user.id)
            self.assertEqual(1, len(TransactionsModel.query.all()))

            data = {"id_transaction": 'string'}  # must be an integer
            with self.assertRaises(Exception):
                TransactionsModel.query.filter_by(id_transaction=1).first().update_from_db(data)

    # TEST TASK 2
    def test_post(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 2, 13.1, "book2")
            book2.save_to_db()

            isbns = [self.book.isbn, book2.isbn]
            quantities = [1, 1]
            dataTransaction = {
                "isbns": isbns,
                'quantities': quantities,
                "email": self.user.email,
            }
            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            # hi ha dues transaccions amb id 1
            self.assertEqual(201, res.status_code)
            transactions = TransactionsModel.find_by_id(1)

            # les dues transaccions equivalen als llibres que acabem de posar
            self.assertEqual(len(transactions), 2)

            for i in range(len(isbns)):
                self.assertEqual(transactions[i].isbn, BooksModel.find_by_isbn(isbns[i]).isbn)

    def test_post_no_stock(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 0, 13.1, "book2")
            book2.save_to_db()

            isbns = [self.book.isbn, book2.isbn]
            quantities = [1, 100]  # no stock!
            dataTransaction = {
                "isbns": isbns,
                'quantities': quantities,
                "email": self.user.email,
            }
            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(500, res.status_code)

    def test_post_wrong_isbn(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 0, 13.1, "book2")
            book2.save_to_db()

            isbns = [100, book2.isbn]
            quantities = [1, 100]  # no stock!
            dataTransaction = {
                "isbns": isbns,
                'quantities': quantities,
                "email": self.user.email,
            }
            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(404, res.status_code)

    # TEST TASK 3
    # test manual: posar variable config TESTING = False i veure com es reb el mail correctament.
    def test_order_mail(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 2, 13.1, "book2")
            book2.save_to_db()

            isbns = [self.book.isbn, book2.isbn]
            quantities = [1, 1]
            dataTransaction = {
                "isbns": isbns,
                'quantities': quantities,
                "email": self.user.email,
            }
            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            # hi ha dues transaccions amb id 1
            self.assertEqual(201, res.status_code)
            transactions = TransactionsModel.find_by_id(1)

            # les dues transaccions equivalen als llibres que acabem de posar
            self.assertEqual(len(transactions), 2)
            for i in range(len(isbns)):
                self.assertEqual(transactions[i].isbn, BooksModel.find_by_isbn(isbns[i]).isbn)

    # TEST TASK 6
    def test_get_transactions_user(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 2, 13.1, "book2")
            book2.save_to_db()

            isbns = [self.book.isbn, book2.isbn]
            quantities = [1, 1]
            dataTransaction = {
                "isbns": isbns,
                'quantities': quantities,
                "email": self.user.email,
            }

            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            # falta relacio!!!

            res = self.client.get(f"/transactions/{self.user.email}", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)
            self.assertEqual(2, len(self.user.transactions))

    def test_get_transactions_without_login(self):
        with self.app.app_context():
            user = UsersModel('test', 'bookshelterES@gmail.com')
            user.hash_password('test')
            UsersModel.save_to_db(user)

            book = BooksModel(1, 1, 1.0, "titulo")
            book.save_to_db()

            # no login

            dataTransaction = {
            }

            res = self.client.post("/transaction", data=dataTransaction)
            self.assertEqual(401, res.status_code)

    def test_get_transactions_other_user(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 2, 13.1, "book2")
            book2.save_to_db()

            isbns = [self.book.isbn, book2.isbn]
            quantities = [1, 1]
            dataTransaction = {
                "isbns": isbns,
                'quantities': quantities,
                "email": self.user.email,
            }

            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            user2 = UsersModel('test2', 'patata@gmail.com')
            user2.hash_password('test2')
            UsersModel.save_to_db(user2)

            res = self.client.get('/transactions/' + user2.email, headers={  # user tries to get user2 transactions
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(401, res.status_code)


if __name__ == '__main__':
    unittest.main()
