import base64
import unittest
import json

from model.books import BooksModel
from model.users import UsersModel, Roles
from model.transactions import TransactionsModel
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):
    def tearDown(self):
        super().tearDown()
        with self.app.app_context():
            TransactionsModel.it_transaction = 1

    def basic_setup(self):
        self.user = UsersModel("test", "bookshelterES@gmail.com", role=Roles.Admin)
        self.user.hash_password("test")
        self.user.save_to_db()

        self.book = BooksModel(1, 1, 1, "book1")
        self.book.save_to_db()

        res = self.client.post("/api/login", data={"email": self.user.email, "password": "test"})
        self.token = json.loads(res.data)["token"]

    def test_get_all_transactions(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 2, 13.1, "book2")
            book2.save_to_db()

            isbns = [self.book.isbn, book2.isbn]
            prices = [self.book.precio, book2.precio]
            quantities = [1, 1]
            TransactionsModel.save_transaction(self.user.id, isbns, prices, quantities)

            res = self.client.get("/api/allTransactions", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)

            allTransactions = TransactionsModel.query.all()
            for i, transaction in enumerate(allTransactions):
                self.assertEqual(transaction.json(), json.loads(res.data)['transactions'][0][i])

    def test_get_all_transactions_no_admin(self):
        with self.app.app_context():
            user = UsersModel("test", "bookshelterES@gmail.com", role=Roles.User)
            user.hash_password("test")
            user.save_to_db()
            res = self.client.post("/api/login", data={"email": user.email, "password": "test"})
            token = json.loads(res.data)["token"]

            book = BooksModel(1, 1, 1, "book1")
            book.save_to_db()
            book2 = BooksModel(2, 2, 13.1, "book2")
            book2.save_to_db()

            isbns = [book.isbn, book2.isbn]
            prices = [book.precio, book2.precio]
            quantities = [1, 1]
            TransactionsModel.save_transaction(user.id, isbns, prices, quantities)

            res = self.client.get("/api/allTransactions", headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(403, res.status_code)

    def test_get_no_transactions(self):
        with self.app.app_context():
            self.basic_setup()

            res = self.client.get("/api/allTransactions", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)

            allTransactions = TransactionsModel.query.all()
            self.assertEqual(0, len(allTransactions))


if __name__ == '__main__':
    unittest.main()
