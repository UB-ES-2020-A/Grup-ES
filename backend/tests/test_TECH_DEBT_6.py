import base64
import json

from tests.base_test import BaseTest
from model.users import UsersModel, Roles
from model.books import BooksModel
from model.reviews import ReviewsModel


class UnitTestOfUS(BaseTest):

    def admin_setup(self):
        password = "Admin1234"
        self.admin = UsersModel("admin", "admin@gmail.com", Roles.Admin)
        self.admin.hash_password(password)
        self.admin.save_to_db()

        res = self.client.post("/api/login", data={"email": self.admin.email, "password": password})
        self.token = json.loads(res.data)["token"]

    def test_post_user_invalid_syntax(self):
        # Same checks will be done in the put of users
        with self.app.app_context():
            # Username length less than 4
            data = {"username": "ias", "email": "test2@email.com", "password": "Test1234"}
            res = self.client.post("/api/user", data=data)
            self.assertEqual(400, res.status_code)
            self.assertIsNone(UsersModel.find_by_username(data["username"]))

            # email without @
            data = {"username": "test1234", "email": "testemail.com", "password": "Test1234"}
            res = self.client.post("/api/user", data=data)
            self.assertEqual(400, res.status_code)
            self.assertIsNone(UsersModel.find_by_username(data["username"]))

            # email without .
            data = {"username": "test1234", "email": "test@emailcom", "password": "Test1234"}
            res = self.client.post("/api/user", data=data)
            self.assertEqual(400, res.status_code)
            self.assertIsNone(UsersModel.find_by_username(data["username"]))

            # email with invalid characters
            data = {"username": "test1234", "email": "test/()@email.com", "password": "Test1234"}
            res = self.client.post("/api/user", data=data)
            self.assertEqual(400, res.status_code)
            self.assertIsNone(UsersModel.find_by_username(data["username"]))

            # email with ending to short
            data = {"username": "test1234", "email": "test2@email.a", "password": "Test1234"}
            res = self.client.post("/api/user", data=data)
            self.assertEqual(400, res.status_code)
            self.assertIsNone(UsersModel.find_by_username(data["username"]))

            # Password too short
            data = {"username": "test1234", "email": "test2@emailcom", "password": "a"}
            res = self.client.post("/api/user", data=data)
            self.assertEqual(400, res.status_code)
            self.assertIsNone(UsersModel.find_by_username(data["username"]))

            # Password without uppercase
            data = {"username": "test1234", "email": "test2@emailcom", "password": "test1234"}
            res = self.client.post("/api/user", data=data)
            self.assertEqual(400, res.status_code)
            self.assertIsNone(UsersModel.find_by_username(data["username"]))

            # Password without numbers
            data = {"username": "test1234", "email": "test2@emailcom", "password": "TestHola"}
            res = self.client.post("/api/user", data=data)
            self.assertEqual(400, res.status_code)
            self.assertIsNone(UsersModel.find_by_username(data["username"]))

    def post_book_invalid(self, data):
        res = self.client.post("/api/book", data=data, headers={
            "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
        })
        self.assertEqual(400, res.status_code)
        self.assertIsNone(BooksModel.find_by_isbn(data["isbn"]))

    def test_post_book_invalid(self):
        # Same checks will be done in the put of book and in the get of resource SearchBooks.
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
            orig_data = {
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

            data = orig_data.copy()
            data["isbn"] = 1  # ISBN size not 13
            self.post_book_invalid(data)

            data = orig_data.copy()
            data["stock"] = -2  # Stock negative
            self.post_book_invalid(data)

            data = orig_data.copy()
            data["precio"] = -2.5  # Precio negative
            self.post_book_invalid(data)

            data = orig_data.copy()
            data["titulo"] = ""  # Empty titulo
            self.post_book_invalid(data)

            data = orig_data.copy()
            data["autor"] = ""  # Empty autor
            self.post_book_invalid(data)

            data = orig_data.copy()
            data["editorial"] = ""  # Empty editorial
            self.post_book_invalid(data)

            data = orig_data.copy()
            data["sinopsis"] = ""  # Empty sinopsis
            self.post_book_invalid(data)

            data = orig_data.copy()
            data["url_imagen"] = ""  # Empty url_imagen
            self.post_book_invalid(data)

            data = orig_data.copy()
            data["fecha_de_publicacion"] = "2000/01/01"  # Invalid syntax
            self.post_book_invalid(data)

            data = orig_data.copy()
            data["fecha_de_publicacion"] = "1-1-2000"  # Invalid order
            self.post_book_invalid(data)

            data = orig_data.copy()
            data["fecha_de_publicacion"] = "2000-1-0"  # Invalid day
            self.post_book_invalid(data)
