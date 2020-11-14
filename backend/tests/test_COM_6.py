import base64
import unittest
import json
from datetime import datetime

from model.books import BooksModel
from model.users import UsersModel
from tests.base_test import BaseTest
from model.transactions import TransactionsModel


class UnitTestOfUS(BaseTest):

    # TEST TASK 1
    def test_model_add(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'bookshelterES@gmail.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)
            entry = TransactionsModel(1, 2.2, 1, 1, None)
            entry.save_to_db()
            self.assertEqual(entry, TransactionsModel.find_by_id(1))

    def test_model_delete(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'bookshelterES@gmail.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)
            entry = TransactionsModel(1, 2.2, 1, 1, None)
            entry.save_to_db()
            entry.delete_from_db()

            self.assertEqual(TransactionsModel.find_by_id(1), None)

    def test_model_update(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'bookshelterES@gmail.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)
            entry = TransactionsModel(1, 2, 1, 1, None)  # id_transaction = 1 -> es automatica
            entry.save_to_db()

            data = {"id_transaction": 10}  # id = 10
            entry.update_from_db(data)

            date = datetime.now()
            book = BooksModel(1, 1, 1.0, "titulo", "autor", "editorial", "sinposis", "url", date)

            book.save_to_db()
            self.assertEqual(book, BooksModel.find_by_isbn(book.isbn))
            self.assertEqual(entry.json(), TransactionsModel.find_by_id(10).json())

    def test_model_invalid_update(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'bookshelterES@gmail.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)

            entry = TransactionsModel(1, 2.2, 1, 1, None)
            entry.save_to_db()

            with self.assertRaises(Exception):
                data = {"isbn": "patata"}  # has to be integer
                entry.update_from_db(data)

    # TEST TASK 2
    def test_post(self):
        with self.app.app_context():
            user = UsersModel('test', 'bookshelterES@gmail.com')
            user.hash_password('test')
            UsersModel.save_to_db(user)
            dataTransaction = {
                "isbn": 1,
                "price": 7.9,
                "email": user.email,
                "quantity": 1
            }
            res = self.client.post("/login", data={"email": user.email, "password": "test"})
            token = json.loads(res.data)["token"]

            data = {
                "isbn": 1,
                "stock": 10,
                "precio": 7.79,
                "titulo": "Foundation",
                "autor": "Isaac Asimov",
                "editorial": "Bantam Books",
                "sinopsis": "sinopsis",
                "url_imagen": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1417900846l"
                              "/29579.jpg",
                "fecha_de_publicacion": "2001-06-01"
            }

            res = self.client.post("/book", data=data)
            self.assertEqual(201, res.status_code)

            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            self.assertEqual(json.loads(res.data), TransactionsModel.query.first().json())  # json.loads(res.data))

    # TEST TASK 3
    def test_order_mail(self):
        with self.app.app_context():
            user = UsersModel('test', 'bookshelterES@gmail.com')
            user.hash_password('test')
            UsersModel.save_to_db(user)
            dataTransaction = {
                "isbn": 1,
                "price": 7.9,
                "email": user.email,
                "quantity": 1
            }
            res = self.client.post("/login", data={"email": user.email, "password": "test"})
            token = json.loads(res.data)["token"]

            data = {
                "isbn": 1,
                "stock": 10,
                "precio": 7.79,
                "titulo": "Foundation",
                "autor": "Isaac Asimov",
                "editorial": "Bantam Books",
                "sinopsis": "sinopsis",
                "url_imagen": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1417900846l"
                              "/29579.jpg",
                "fecha_de_publicacion": "2001-06-01"
            }

            res = self.client.post("/book", data=data)
            self.assertEqual(201, res.status_code)

            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            self.assertEqual(json.loads(res.data), TransactionsModel.query.first().json())


    # TEST TASK 6
    def test_get_transactions_user(self):
        with self.app.app_context():
            user = UsersModel('test', 'bookshelterES@gmail.com')
            user.hash_password('test')
            UsersModel.save_to_db(user)
            dataTransaction = {
                "isbn": 1,
                "price": 7.9,
                "email": user.email,
                "quantity": 1
            }
            res = self.client.post("/login", data={"email": user.email, "password": "test"})
            token = json.loads(res.data)["token"]


            data = {
                "isbn": 1,
                "stock": 10,
                "precio": 7.79,
                "titulo": "Foundation",
                "autor": "Isaac Asimov",
                "editorial": "Bantam Books",
                "sinopsis": "sinopsis",
                "url_imagen": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1417900846l"
                              "/29579.jpg",
                "fecha_de_publicacion": "2001-06-01"
            }

            res = self.client.post("/book", data=data)
            self.assertEqual(201, res.status_code)

            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)

            res = self.client.get('/transactions/' + user.email, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })  # transactions del user amb id = 1
            self.assertEqual(200, res.status_code)
            self.assertEqual(len(json.loads(res.data)), 1)

            self.assertEqual([TransactionsModel.find_by_id(1).json()], json.loads(res.data)["transactions"])

    def test_get_transactions_without_login(self):
        with self.app.app_context():
            user = UsersModel('test', 'bookshelterES@gmail.com')
            user.hash_password('test')
            UsersModel.save_to_db(user)
            dataTransaction = {
                "isbn": 1,
                "price": 7.9,
                "email": user.email,
                "quantity": 1
            }
            data = {
                "isbn": 1,
                "stock": 10,
                "precio": 7.79,
                "titulo": "Foundation",
                "autor": "Isaac Asimov",
                "editorial": "Bantam Books",
                "sinopsis": "sinopsis",
                "url_imagen": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1417900846l"
                              "/29579.jpg",
                "fecha_de_publicacion": "2001-06-01"
            }

            res = self.client.post("/book", data=data)
            self.assertEqual(201, res.status_code)

            res = self.client.post("/transaction", data=dataTransaction)
            self.assertEqual(401, res.status_code)

    def test_get_transactions_other_user(self):
        with self.app.app_context():
            user = UsersModel('test', 'bookshelterES@gmail.com')
            user.hash_password('test')
            UsersModel.save_to_db(user)

            user2 = UsersModel('test2', 'mail@gmail.com')
            user2.hash_password('test2')
            UsersModel.save_to_db(user2)

            dataTransaction = {
                "isbn": 1,
                "price": 7.9,
                "email": user.email,
                "quantity": 1
            }
            res = self.client.post("/login", data={"email": user.email, "password": "test"})
            token = json.loads(res.data)["token"]

            data = {
                "isbn": 1,
                "stock": 10,
                "precio": 7.79,
                "titulo": "Foundation",
                "autor": "Isaac Asimov",
                "editorial": "Bantam Books",
                "sinopsis": "sinopsis",
                "url_imagen": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1417900846l"
                              "/29579.jpg",
                "fecha_de_publicacion": "2001-06-01"
            }

            res = self.client.post("/book", data=data)
            self.assertEqual(201, res.status_code)

            res = self.client.post("/transaction", data=dataTransaction, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)

            res = self.client.get('/transactions/' + user2.email, headers={  #user tries to get user2 transactions
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(401, res.status_code)


if __name__ == '__main__':
    unittest.main()
