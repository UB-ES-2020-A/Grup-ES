import base64
import unittest
import json
import datetime as dt

from model.books import BooksModel
from model.library import LibraryModel, LibraryType, State
from model.users import UsersModel
from tests.base_test import BaseTest
from model.transactions import TransactionsModel


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
            expected = TransactionsModel.save_transaction(self.user.id, [self.book.isbn], [self.book.precio], [1])
            self.assertEqual(expected[0], TransactionsModel.find_by_id_and_isbn(1, self.book.isbn).json())

            expected = TransactionsModel.save_transaction(self.user.id, [book2.isbn], [self.book.precio], [1])
            self.assertEqual(expected[0], TransactionsModel.find_by_id_and_isbn(2, book2.isbn).json())

    def test_model_add_some(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 1, 1, "book2")
            book2.save_to_db()

            expected = TransactionsModel.save_transaction(self.user.id, [self.book.isbn, book2.isbn],
                                                          [self.book.precio, book2.precio], [1, 1])
            self.assertEqual(expected[0], TransactionsModel.find_by_id_and_isbn(1, self.book.isbn).json())
            self.assertEqual(expected[1], TransactionsModel.find_by_id_and_isbn(1, book2.isbn).json())  # same id

    def test_model_add_no_stock(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 1, 1, "book2")
            book2.save_to_db()

            with self.assertRaises(Exception):
                TransactionsModel.save_transaction(self.user.id, [self.book.isbn], [self.book.precio], [100])

    def test_model_delete(self):
        with self.app.app_context():
            self.basic_setup()

            TransactionsModel.save_transaction(self.user.id, [self.book.isbn], [self.book.precio], [1])
            self.assertEqual(1, len(TransactionsModel.query.all()))

            TransactionsModel.query.filter_by(id_transaction=1).first().delete_from_db()
            self.assertEqual(0, len(TransactionsModel.query.all()))

    def test_model_update(self):
        with self.app.app_context():
            self.basic_setup()

            TransactionsModel.save_transaction(self.user.id, [self.book.isbn], [self.book.precio], [1])
            self.assertEqual(1, len(TransactionsModel.query.all()))

            data = {"id_transaction": 10}  # id = 10
            TransactionsModel.query.filter_by(id_transaction=1).first().update_from_db(data)
            expected_output = {'date': dt.datetime.today().strftime("%d-%m-%Y"),
                               'id_transaction': 10,
                               'user_id': 1,
                               'isbn': self.book.isbn,
                               'price': self.book.precio,
                               'book': self.book.json(),
                               'quantity': 1}

            self.assertEqual(expected_output, TransactionsModel.find_by_id(data["id_transaction"])[0].json())

    def test_model_invalid_update(self):
        with self.app.app_context():
            self.basic_setup()

            TransactionsModel.save_transaction(self.user.id, [self.book.isbn], [self.book.precio], [1])
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
            prices = [self.book.precio, book2.precio]
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

    def test_post_add_library(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 10, 13.1, "book2")
            book2.save_to_db()

            isbns = [self.book.isbn, book2.isbn]
            prices = [self.book.precio, book2.precio]
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
            self.assertEqual(self.book.isbn, self.user.library[0].isbn)
            self.assertEqual(book2.isbn, self.user.library[1].isbn)
            self.assertEqual(2, len(self.user.library))

    def test_post_add_library_delete_from_wishlist(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 10, 13.1, "book2")
            book2.save_to_db()

            # enter book to wishlist
            entry = LibraryModel(self.book.isbn, 1, LibraryType.WishList, State.Pending)
            entry.save_to_db()
            self.assertEqual(entry, LibraryModel.find_by_id_and_isbn(1, 1))

            isbns = [self.book.isbn, book2.isbn]
            prices = [self.book.precio, book2.precio]
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

            # check if book is in library
            self.assertEqual(self.book.isbn, self.user.library[0].isbn)
            self.assertEqual(book2.isbn, self.user.library[1].isbn)

            # check if type of book2 has changed: was in wishlist, now bought
            self.assertEqual(LibraryType.Bought, self.user.library[1].library_type)

            self.assertEqual(2, len(self.user.library))

    def test_post_no_stock(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 0, 13.1, "book2")
            book2.save_to_db()

            isbns = [self.book.isbn, book2.isbn]
            prices = [self.book.precio, book2.precio]
            quantities = [1, 100]  # no stock!
            dataTransaction = {
                "isbns": isbns,
                'prices': prices,
                'quantities': quantities,
                "email": self.user.email,
            }
            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(404, res.status_code)

    def test_post_wrong_isbn(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 0, 13.1, "book2")
            book2.save_to_db()

            isbns = [100, book2.isbn]  # wrong isbn
            prices = [self.book.precio, book2.precio]
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
            self.assertEqual(404, res.status_code)

    # TEST TASK 3
    # test manual: posar variable config TESTING = False i veure com es reb el mail correctament.
    def test_order_mail(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 2, 13.1, "book2")
            book2.save_to_db()

            isbns = [self.book.isbn, book2.isbn]
            prices = [self.book.precio, book2.precio]
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

    # TEST TASK 6
    def test_get_transactions_user(self):
        with self.app.app_context():
            self.basic_setup()
            book2 = BooksModel(2, 2, 13.1, "book2")
            book2.save_to_db()

            isbns = [self.book.isbn, book2.isbn]
            prices = [self.book.precio, book2.precio]
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

            res = self.client.get(f"/transactions/{self.user.email}", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)
            # l'usuari te dues transactions
            self.assertEqual(2, len(self.user.transactions))

            # comprovem que son les que hem acabat d'afegir
            expected = [transaction.json() for transaction in TransactionsModel.find_by_id(1)]
            real_output = [transaction.json() for transaction in self.user.transactions]
            self.assertEqual(expected, real_output)

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
            prices = [self.book.precio, book2.precio]
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
            user2 = UsersModel('test2', 'patata@gmail.com')
            user2.hash_password('test2')
            UsersModel.save_to_db(user2)

            res = self.client.get('/transactions/' + user2.email, headers={  # user tries to get user2 transactions
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(401, res.status_code)


if __name__ == '__main__':
    unittest.main()
