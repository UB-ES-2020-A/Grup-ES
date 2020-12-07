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
        self.book2 = BooksModel(2, 100, 13.1, "book2")
        self.book2.save_to_db()

        res = self.client.post("/api/login", data={"email": self.user.email, "password": "test"})
        self.token = json.loads(res.data)["token"]

    def test_get_best_sellers(self):
        with self.app.app_context():
            self.basic_setup()

            isbns = [self.book.isbn, self.book2.isbn]
            prices = [self.book.precio, self.book2.precio]
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
<<<<<<< HEAD
            res = self.client.get('/api/trending', data=args)
            self.assertEqual(200, res.status_code)

            self.assertEqual(2, len(json.loads(res.data)['books']))  # veiem que n'hi ha dos com li hem demanat
=======
            res = self.client.get('/trending', data=args)
            self.assertEqual(200, res.status_code)

            self.assertEqual(len(json.loads(res.data)['books']), 2)  # veiem que n'hi ha dos com li hem demanat
>>>>>>> dev
            self.assertEqual(self.book2.isbn, json.loads(res.data)['books'][0]['isbn'])  # el més venut és el llibre amb isbn 2

    def test_get_best_sellers_2(self):
        with self.app.app_context():
            self.basic_setup()

            isbns = [self.book.isbn, self.book2.isbn]
            prices = [self.book.precio, self.book2.precio]
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
<<<<<<< HEAD
            res = self.client.get('/api/trending', data=args)
            self.assertEqual(200, res.status_code)

            self.assertEqual(1, len(json.loads(res.data)['books']))  # ens retorna només 1
=======
            res = self.client.get('/trending', data=args)
            self.assertEqual(200, res.status_code)

            self.assertEqual(len(json.loads(res.data)['books']), 1)  # ens retorna només 1
>>>>>>> dev
            self.assertEqual(self.book2.isbn, json.loads(res.data)['books'][0]['isbn'])  # el més venut és el llibre amb isbn 2

    def test_get_best_sellers_no_transactions(self):
        with self.app.app_context():
            self.basic_setup()
            args = {
                "numBooks": 1,
            }
<<<<<<< HEAD
            res = self.client.get('/api/trending', data=args)
            self.assertEqual(200, res.status_code)

            self.assertEqual(0, len(json.loads(res.data)['books']))  # encara que el numBooks sigui 1, retorna 0 perque no
=======
            res = self.client.get('/trending', data=args)
            self.assertEqual(200, res.status_code)

            self.assertEqual(len(json.loads(res.data)['books']), 0)  # encara que el numBooks sigui 1, retorna 0 perque no
>>>>>>> dev
            # hi ha cap transaction

    def test_get_best_sellers_no_vendible(self):
        with self.app.app_context():
            self.basic_setup()

            self.book2.vendible = False

            isbns = [self.book.isbn, self.book2.isbn]
            prices = [self.book.precio, self.book2.precio]
            quantities = [1, 50]
            dataTransaction = {
                "isbns": isbns,
                'prices': prices,
                'quantities': quantities,
                "email": self.user.email,
            }
<<<<<<< HEAD
            res = self.client.post("/api/transaction", data=dataTransaction, headers={
=======
            res = self.client.post("/transaction", data=dataTransaction, headers={
>>>>>>> dev
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)

            args = {
                "numBooks": 1,
            }
<<<<<<< HEAD
            res = self.client.get('/api/trending', data=args)
=======
            res = self.client.get('/trending', data=args)
>>>>>>> dev
            self.assertEqual(200, res.status_code)

            # el llibre amb isbn=2 no és vendible així que el llibre més venut és el isbn=1.
            self.assertEqual(self.book.isbn, json.loads(res.data)['books'][0]['isbn'])


if __name__ == '__main__':
    unittest.main()
