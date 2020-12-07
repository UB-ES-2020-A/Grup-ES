import base64
import json
import unittest

from model.books import BooksModel
from model.transactions import TransactionsModel
from model.users import UsersModel
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):

    def basic_setup(self):
        self.user = UsersModel("test", "bookshelterES@gmail.com")
        self.user.hash_password("test")
        self.user.save_to_db()

        self.book = BooksModel(1, 1, 1, "book1")
        self.book.save_to_db()

        res = self.client.post("/api/login", data={"email": self.user.email, "password": "test"})
        self.token = json.loads(res.data)["token"]

    def test_get_best_sellers(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 100, 13.1, "book2")
            book2.save_to_db()

            isbns = [self.book.isbn, book2.isbn]
            prices = [self.book.precio, book2.precio]
            quantities = [1, 50]
            dataTransaction = {
                "isbns": isbns,
                'prices': prices,
                'quantities': quantities,
                "email": self.user.email,
            }
            res = self.client.post("/api/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            # hi ha dues transaccions amb id 1
            transactions = TransactionsModel.find_by_id(1)
            self.assertEqual(len(transactions), 2)

            args = {
                "numBooks": 2,
            }
            res = self.client.get('/api/trending', data=args)
            self.assertEqual(200, res.status_code)

            self.assertEqual(len(json.loads(res.data)['books']), 2)  # veiem que n'hi ha dos com li hem demanat
            self.assertEqual(json.loads(res.data)['books'][0]['isbn'], 2)  # el més venut és el llibre amb isbn 2

    def test_get_best_sellers_2(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 100, 13.1, "book2")
            book2.save_to_db()

            isbns = [self.book.isbn, book2.isbn]
            prices = [self.book.precio, book2.precio]
            quantities = [1, 50]
            dataTransaction = {
                "isbns": isbns,
                'prices': prices,
                'quantities': quantities,
                "email": self.user.email,
            }
            res = self.client.post("/api/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)

            args = {
                "numBooks": 1,
            }
            res = self.client.get('/api/trending', data=args)
            self.assertEqual(200, res.status_code)

            self.assertEqual(len(json.loads(res.data)['books']), 1)  # ens retorna només 1
            self.assertEqual(json.loads(res.data)['books'][0]['isbn'], 2)  # el més venut és el llibre amb isbn 2

    def test_get_best_sellers_no_transactions(self):
        with self.app.app_context():
            self.basic_setup()
        args = {
            "numBooks": 1,
        }
        res = self.client.get('/api/trending', data=args)
        self.assertEqual(200, res.status_code)

        self.assertEqual(len(json.loads(res.data)['books']), 0)  # encara que el numBooks sigui 1, retorna 0 perque no
        # hi ha cap transaction


if __name__ == '__main__':
    unittest.main()
