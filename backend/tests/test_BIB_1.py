import base64
import json
import unittest

from tests.base_test import BaseTest
from model.library import LibraryModel, LibraryType
from model.users import UsersModel
from model.books import BooksModel
# Solves problem of user model not finding reviews model
from model.reviews import ReviewsModel


class UnitTestOfUS(BaseTest):

    def basic_setup(self):
        password = "test"
        self.user = UsersModel("test", "test")
        self.user.hash_password(password)
        self.user.save_to_db()

        self.book = BooksModel(1, 10, 10, "test")
        self.book.save_to_db()

        self.entry = LibraryModel(self.book.isbn, self.user.id, LibraryType.Bought)
        self.entry.save_to_db()

        res = self.client.post("/login", data={"email": self.user.email, "password": password})
        self.token = json.loads(res.data)["token"]

    # TEST TASK 1
    def test_delete_library_visibility(self):
        with self.app.app_context():
            self.basic_setup()

            res = self.client.delete(f"/library/{self.user.email}/{self.book.isbn}", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })

            self.assertEqual(200, res.status_code)
            self.assertEqual(False, LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).visible)

    def test_post_library_visibility(self):
        with self.app.app_context():
            self.basic_setup()
            self.entry.change_visible_db(False)

            res = self.client.post(f"/library/{self.user.email}/{self.book.isbn}", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })

            self.assertEqual(200, res.status_code)
            self.assertEqual(True, LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).visible)

    # Endpoint independent
    def test_library_visibility_invalid_email(self):
        with self.app.app_context():
            self.basic_setup()

            res = self.client.delete(f"/library/fails/{self.book.isbn}", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })

            self.assertEqual(404, res.status_code)
            # Checks visibility doesn't change
            self.assertEqual(self.entry.visible, LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).visible)

    def test_library_visibility_invalid_isbn(self):
        with self.app.app_context():
            self.basic_setup()

            res = self.client.delete(f"/library/{self.user.email}/fails", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })

            self.assertEqual(404, res.status_code)
            # Checks visibility doesn't change
            self.assertEqual(self.entry.visible, LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).visible)

    def test_library_visibility_modification_other_user(self):
        with self.app.app_context():
            self.basic_setup()

            user2 = UsersModel("test2", "test2")
            user2.hash_password("test2")
            user2.save_to_db()

            library = self.entry = LibraryModel(self.book.isbn, user2.id, LibraryType.Bought)
            library.save_to_db()

            res = self.client.delete(f"/library/{user2.email}/{self.book.isbn}", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })

            self.assertEqual(401, res.status_code)
            # Checks visibility doesn't change
            self.assertEqual(self.entry.visible, LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).visible)

    def test_library_visibility_not_logged(self):
        with self.app.app_context():
            self.basic_setup()

            res = self.client.delete(f"/library/{self.user.email}/{self.book.isbn}")

            self.assertEqual(401, res.status_code)
            # Checks visibility doesn't change
            self.assertEqual(self.entry.visible, LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).visible)


if __name__ == '__main__':
    unittest.main()
