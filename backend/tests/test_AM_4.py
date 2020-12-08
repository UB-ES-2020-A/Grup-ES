import base64
import unittest
import json

from model.books import BooksModel
from model.users import UsersModel, Roles
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):

    def basic_setup(self):
        self.user = UsersModel("test", "bookshelterES@gmail.com", role=Roles.Admin)
        self.user.hash_password("test")
        self.user.save_to_db()

        res = self.client.post("/api/login", data={"email": self.user.email, "password": "test"})
        self.token = json.loads(res.data)["token"]

        self.sinopsis = "For twelve thousand years the Galactic Empire has ruled supreme. Now it is dying. But only " \
                   "Hari Seldon, creator of the revolutionary science of psychohistory, can see into the future " \
                   "-- to a dark age of ignorance, barbarism, and warfare that will last thirty thousand years. " \
                   "To preserve knowledge and save mankind, Seldon gathers the best minds in the Empire -- both " \
                   "scientists and scholars -- and brings them to a bleak planet at the edge of the Galaxy to " \
                   "serve as a beacon of hope for a future generations. He calls his sanctuary the " \
                   "Foundation.\nBut soon the fledgling Foundation finds itself at the mercy of corrupt warlords " \
                   "rising in the wake of the receding Empire. Mankind's last best hope is faced with an " \
                   "agonizing choice: submit to the barbarians and be overrun -- or fight them and be destroyed. "
        self.isbn = 9780553803716
        self.data_new = {
            "sinopsis": self.sinopsis,
            "precio": 8.60,
            "stock": 9
        }
        self.data_old = {
            "isbn": self.isbn,
            "stock": 10,
            "precio": 7.79,
            "titulo": "Foundation",
            "autor": "Isaac Asimov",
            "editorial": "Bantam Books",
            "url_imagen": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1417900846l"
                          "/29579.jpg",
            "fecha_de_publicacion": "2001-06-01"
        }

    # TEST TASK 2
    def test_basic_put_book(self):
        with self.app.app_context():
            self.basic_setup()
            res = self.client.post("/api/book", data=self.data_old, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)

            self.assertEqual(BooksModel.find_by_isbn(self.isbn).json(), json.loads(res.data))
            res = self.client.put(f"/api/book/{self.isbn}", data=self.data_new, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)

    def test_basic_put_book_no_admin(self):
        with self.app.app_context():
            self.basic_setup()
            res = self.client.post("/api/book", data=self.data_old, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)

            self.assertEqual(BooksModel.find_by_isbn(self.isbn).json(), json.loads(res.data))
            res = self.client.put(f"/api/book/{self.isbn}", data=self.data_new)
            self.assertEqual(401, res.status_code)

    # TEST TASK 2
    def test_basic_put_book_vendible(self):
        with self.app.app_context():
            self.basic_setup()
            data_new = {
                "sinopsis": self.sinopsis,
                "precio": 8.60,
                "stock": 9,
                "vendible": False
            }

            res = self.client.post("/api/book", data=self.data_old, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            self.assertEqual(BooksModel.find_by_isbn(self.isbn).json(), json.loads(res.data))

            res = self.client.put(f"/api/book/{self.isbn}", data=self.data_new, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)


if __name__ == '__main__':
    unittest.main()
