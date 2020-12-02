import base64
import unittest
import json

from model.books import BooksModel
from model.users import UsersModel
from model.transactions import TransactionsModel
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):
    def tearDown(self):
        super().tearDown()
        with self.app.app_context():
            TransactionsModel.it_transaction = 1

    def basic_setup(self):
        self.user = UsersModel("test", "bookshelterES@gmail.com", role='Admin')
        self.user.hash_password("test")
        self.user.save_to_db()
        self.user2 = UsersModel("test2", "mail@gmail.com", role='User')
        self.user2.hash_password("test2")
        self.user2.save_to_db()

        self.book = BooksModel(1, 100, 1, "book1")
        self.book.save_to_db()
        self.book2 = BooksModel(2, 50, 13.1, "book2")
        self.book2.save_to_db()

        res = self.client.post("/login", data={"email": self.user.email, "password": "test"})
        self.token = json.loads(res.data)["token"]
        res = self.client.post("/login", data={"email": self.user2.email, "password": "test2"})
        self.token2 = json.loads(res.data)["token"]

    def add_transactions_user1(self):
        isbns = [self.book.isbn, self.book2.isbn]
        prices = [self.book.precio, self.book2.precio]
        quantities = [1, 1]
        dataTransaction = {
            "isbns": isbns,
            'prices': prices,
            'quantities': quantities,
            "email": self.user.email,
        }
        res = self.client.post("/transaction", data=dataTransaction, headers={
            "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
        })
        self.assertEqual(201, res.status_code)
        # hi ha dues transaccions amb id 1
        transactions = TransactionsModel.find_by_id(1)
        self.assertEqual(len(transactions), 2)

        # les dues transaccions equivalen als llibres que acabem de posar
        for i, isbn in enumerate(isbns):
            self.assertEqual(TransactionsModel.find_by_id_and_isbn(1, isbn).json(),
                             json.loads(res.data)['transactions'][i])

    def add_transactions_user2(self):
        isbns = [self.book.isbn, self.book2.isbn]
        prices = [self.book.precio, self.book2.precio]
        quantities = [3, 1]
        dataTransaction = {
            "isbns": isbns,
            'prices': prices,
            'quantities': quantities,
            "email": self.user2.email,
        }
        res = self.client.post("/transaction", data=dataTransaction, headers={
            "Authorization": 'Basic ' + base64.b64encode((self.token2 + ":").encode('ascii')).decode('ascii')
        })
        self.assertEqual(201, res.status_code)
        # hi ha dues transaccions amb id 1
        transactions = TransactionsModel.find_by_id(2)
        self.assertEqual(len(transactions), 2)

        # les dues transaccions equivalen als llibres que acabem de posar
        for i, isbn in enumerate(isbns):
            self.assertEqual(TransactionsModel.find_by_id_and_isbn(2, isbn).json(),
                             json.loads(res.data)['transactions'][i])

    # TASK 2
    def test_get_all_transactions_no_filter(self):
        with self.app.app_context():
            self.basic_setup()
            self.add_transactions_user1()
            self.add_transactions_user2()

            res = self.client.get("/allTransactions", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)

            allTransactions = TransactionsModel.query.all()
            self.assertEqual(4, len(allTransactions))
            # no se com comprovar que son les que hi ha afegides.

    def test_filter_transactions_by_isbn(self):
        with self.app.app_context():
            self.basic_setup()
            self.add_transactions_user1()

            res = self.client.get("/allTransactions", data={'isbn': self.book.isbn}, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)

            transactions = TransactionsModel.query.filter_by(isbn=self.book.isbn).all()
            for i, transaction in enumerate(transactions):
                self.assertEqual(transaction.json(), json.loads(res.data)['transactions'][0][i])

    def test_filter_transactions_by_user_id(self):
        with self.app.app_context():
            self.basic_setup()
            self.add_transactions_user1()
            self.add_transactions_user2()

            res = self.client.get("/allTransactions", data={'user_id': self.user2.id}, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)

            transactions = TransactionsModel.query.filter_by(user_id=self.user.id).all()
            for transaction_id in json.loads(res.data)['transactions']:
                for transaction in transaction_id:
                    self.assertEqual(self.user2.id, transaction['user_id'])

    def test_filter_transactions_by_user_id_and_date_desc(self):
        with self.app.app_context():
            self.basic_setup()
            self.add_transactions_user1()
            self.add_transactions_user2()

            res = self.client.get("/allTransactions", data={'user_id': self.user2.id, 'date': 'desc'}, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)

    def test_get_no_transactions(self):
        with self.app.app_context():
            self.basic_setup()

            res = self.client.get("/allTransactions", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)

            allTransactions = TransactionsModel.query.all()
            self.assertEqual(0, len(allTransactions))


if __name__ == '__main__':
    unittest.main()
