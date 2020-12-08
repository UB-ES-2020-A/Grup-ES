import base64
import unittest
import json
from datetime import datetime

from model.books import BooksModel
from model.users import UsersModel, Roles
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):

    def admin_setup(self):
        password = "admin"
        self.admin = UsersModel("admin", "admin", Roles.Admin)
        self.admin.hash_password(password)
        self.admin.save_to_db()

        res = self.client.post("/api/login", data={"email": self.admin.email, "password": password})
        self.token = json.loads(res.data)["token"]

    # TEST TASK 1
    def test_model_add(self):
        with self.app.app_context():
            date = datetime.now()
            book = BooksModel(1, 1, 1.0, "titulo", "autor", "editorial", "sinposis", "url", date)

            book.save_to_db()
            self.assertEqual(book, BooksModel.find_by_isbn(book.isbn))

    def test_model_add_duplicate(self):
        with self.app.app_context():
            date = datetime.now()
            book = BooksModel(1, 1, 1.0, "titulo", "autor", "editorial", "sinposis", "url", date)
            book.save_to_db()

            same_book = BooksModel(1, 1, 1.0, "titulo", "autor", "editorial", "sinposis", "url", date)
            with self.assertRaises(Exception):
                same_book.save_to_db()

    def test_model_delete(self):
        with self.app.app_context():
            date = datetime.now()
            book = BooksModel(1, 1, 1.0, "titulo", "autor", "editorial", "sinposis", "url", date)

            book.save_to_db()
            book.delete_from_db()
            self.assertEqual(False, book.vendible)

    # TEST TASK 2
    def test_post_book(self):
        with self.app.app_context():
            self.admin_setup()

            sinopsis = "For twelve thousand years the Galactic Empire has ruled supreme. Now it is dying. But only " \
                       "Hari Seldon, creator of the revolutionary science of psychohistory, can see into the future " \
                       "-- to a dark age of ignorance, barbarism, and warfare that will last thirty thousand years. " \
                       "To preserve knowledge and save mankind, Seldon gathers the best minds in the Empire -- both " \
                       "scientists and scholars -- and brings them to a bleak planet at the edge of the Galaxy to " \
                       "serve as a beacon of hope for a future generations. He calls his sanctuary the " \
                       "Foundation.\nBut soon the fledgling Foundation finds itself at the mercy of corrupt warlords " \
                       "rising in the wake of the receding Empire. Mankind's last best hope is faced with an " \
                       "agonizing choice: submit to the barbarians and be overrun -- or fight them and be destroyed. "
            isbn = 9780553803716
            data = {
                "isbn": isbn,
                "stock": 10,
                "precio": 7.79,
                "titulo": "Foundation",
                "autor": "Isaac Asimov",
                "editorial": "Bantam Books",
                "sinopsis": sinopsis,
                "url_imagen": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1417900846l"
                              "/29579.jpg",
                "fecha_de_publicacion": "2001-06-01"
            }

            res = self.client.post("/api/book", data=data, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            self.assertEqual(BooksModel.find_by_isbn(isbn).json(), json.loads(res.data))

            res = self.client.post("/api/book", data=data, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(409, res.status_code)

    def test_post_book_with_minimum_attributes(self):
        with self.app.app_context():
            self.admin_setup()

            isbn = 9780553803716
            data = {
                "isbn": isbn,
                "stock": 10,
                "precio": 7.79,
                "titulo": "Foundation",
            }

            res = self.client.post("/api/book", data=data, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            self.assertEqual(BooksModel.find_by_isbn(isbn).json(), json.loads(res.data))

            res = self.client.post("/api/book", data=data, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(409, res.status_code)

    def test_post_book_with_less_than_minimum_attributes(self):
        with self.app.app_context():
            self.admin_setup()

            isbn = 9780553803716
            data = {
                "isbn": isbn,
                "titulo": "Foundation",
            }

            res = self.client.post("/api/book", data=data, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(400, res.status_code)


if __name__ == '__main__':
    unittest.main()
