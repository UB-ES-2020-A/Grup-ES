import base64
import json
import unittest

from tests.base_test import BaseTest
from model.library import LibraryModel, LibraryType, State
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

        res = self.client.post("/api/login", data={"email": self.user.email, "password": password})
        self.token = json.loads(res.data)["token"]

    # TEST TASK 1
    def test_put_library(self):
        with self.app.app_context():
            self.basic_setup()

            new_data = {
                "state": State.Finished.name,
                "library_type": LibraryType.WishList.name
            }

            res = self.client.put(f"/api/library/{self.user.email}/{self.book.isbn}", data=new_data, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })

            self.assertEqual(200, res.status_code)
            self.assertEqual(State.Finished, LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).state)
            self.assertEqual(LibraryType.WishList,
                             LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).library_type)

    def test_library_visibility_invalid_email(self):
        with self.app.app_context():
            self.basic_setup()

            new_data = {
                "state": State.Finished.name,
                "library_type": LibraryType.WishList.name
            }

            res = self.client.put(f"/api/library/invalid/{self.book.isbn}", data=new_data, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })

            self.assertEqual(404, res.status_code)
            self.assertEqual(self.entry.state, LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).state)
            self.assertEqual(self.entry.library_type,
                             LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).library_type)

    def test_library_visibility_invalid_isbn(self):
        with self.app.app_context():
            self.basic_setup()

            new_data = {
                "state": State.Finished.name,
                "library_type": LibraryType.WishList.name
            }

            res = self.client.put(f"/api/library/{self.user.email}/invalid", data=new_data, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })

            self.assertEqual(404, res.status_code)
            self.assertEqual(self.entry.state, LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).state)
            self.assertEqual(self.entry.library_type,
                             LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).library_type)

    def test_library_visibility_modification_other_user(self):
        with self.app.app_context():
            self.basic_setup()

            user2 = UsersModel("test2", "test2")
            user2.hash_password("test2")
            user2.save_to_db()

            library = self.entry = LibraryModel(self.book.isbn, user2.id, LibraryType.Bought)
            library.save_to_db()

            new_data = {
                "state": State.Finished.name,
                "library_type": LibraryType.WishList.name
            }

            res = self.client.put(f"/api/library/{user2.email}/{self.book.isbn}", data=new_data, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })

            self.assertEqual(401, res.status_code)
            self.assertEqual(self.entry.state, LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).state)
            self.assertEqual(self.entry.library_type,
                             LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).library_type)

    def test_library_visibility_not_logged(self):
        with self.app.app_context():
            self.basic_setup()

            new_data = {
                "state": State.Finished.name,
                "library_type": LibraryType.WishList.name
            }

            res = self.client.put(f"/api/library/invalid/{self.book.isbn}", data=new_data)

            self.assertEqual(401, res.status_code)
            self.assertEqual(self.entry.state, LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).state)
            self.assertEqual(self.entry.library_type,
                             LibraryModel.find_by_id_and_isbn(self.user.id, self.book.isbn).library_type)


if __name__ == '__main__':
    unittest.main()
