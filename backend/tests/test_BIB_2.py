import base64
import json
import unittest

from model.books import BooksModel
from tests.base_test import BaseTest
from model.library import LibraryModel, LibraryType, State
from model.users import UsersModel


class UnitTestOfUS(BaseTest):

    # TEST TASK 2
    def test_model_add(self):
        with self.app.app_context():
            entry = LibraryModel(1, 1, LibraryType.Bought, State.Dropped)

            entry.save_to_db()
            self.assertEqual(entry, LibraryModel.find_by_id_and_isbn(1, 1))

    def test_model_add_duplicate(self):
        with self.app.app_context():
            entry = LibraryModel(1, 1, LibraryType.WishList, State.Reading)
            entry.save_to_db()

            same_entry = LibraryModel(1, 1, LibraryType.WishList, State.Reading)
            with self.assertRaises(Exception):
                same_entry.save_to_db()

    def test_model_delete(self):
        with self.app.app_context():
            entry = LibraryModel(1, 1, LibraryType.Bought)
            entry.save_to_db()
            entry.delete_from_db()

            self.assertEqual(False, entry.visible)

    def test_model_update(self):
        with self.app.app_context():
            entry = LibraryModel(1, 1, LibraryType.Bought, State.Finished)
            entry.save_to_db()

            data = {"isbn": 2, "user_id": 2, "state": "Reading", "visible": True, "library_type": "WishList"}
            entry.update_from_db(data)

            self.assertEqual(entry.json(), data)

    def test_model_invalid_update(self):
        with self.app.app_context():
            entry = LibraryModel(1, 1, LibraryType.WishList, State.Pending)
            entry.save_to_db()

            with self.assertRaises(Exception):
                data = {"isbn": 1, "user_id": 1, "state": "Pending2", "visible": True, "library_type": "WishList"}
                entry.update_from_db(data)

    # TEST TASK 3
    def test_get_entry(self):
        with self.app.app_context():
            user = UsersModel("test", "test")
            user.hash_password("test")
            user.save_to_db()

            entry = LibraryModel(1, user.id, LibraryType.Bought, State.Pending)
            entry.save_to_db()
            entry2 = LibraryModel(2, user.id, LibraryType.WishList, State.Pending)
            entry2.save_to_db()
            entry3 = LibraryModel(3, user.id, LibraryType.Bought, State.Reading)
            entry3.save_to_db()

            res = self.client.post("/login", data={"email": user.email, "password": "test"})
            token = json.loads(res.data)["token"]

            res = self.client.get(f"/library/{user.email}", headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)
            expectedRes = list(map(lambda e: e.json(), [entry, entry3]))
            self.assertEqual(expectedRes, json.loads(res.data)["library"])

    def test_get_entry_with_parameters(self):
        with self.app.app_context():
            user = UsersModel("test", "test")
            user.hash_password("test2")
            user.save_to_db()

            entry = LibraryModel(4, user.id, LibraryType.Bought, State.Dropped)
            entry.save_to_db()
            entry2 = LibraryModel(5, user.id, LibraryType.WishList, State.Pending)
            entry2.save_to_db()
            entry3 = LibraryModel(6, user.id, LibraryType.Bought, State.Pending)
            entry3.save_to_db()

            res = self.client.post("/login", data={"email": user.email, "password": "test2"})
            token = json.loads(res.data)["token"]

            res = self.client.get(f"/library/{user.email}", data={"library_type": "Bought"}, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)
            expectedRes = list(map(lambda e: e.json(), [entry, entry3]))
            self.assertEqual(expectedRes, json.loads(res.data)["library"])

            res = self.client.get(f"/library/{user.email}", data={"library_type": "WishList"}, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)
            expectedRes = list(map(lambda e: e.json(), [entry2]))
            self.assertEqual(expectedRes, json.loads(res.data)["library"])

    def test_get_entry_without_login(self):
        with self.app.app_context():
            user = UsersModel("test", "test")
            user.hash_password("test3")
            user.save_to_db()

            res = self.client.get(f"/library/{user.email}")
            self.assertEqual(401, res.status_code)

    def test_get_entry_invalid_parameter(self):
        with self.app.app_context():
            user = UsersModel("test", "test")
            user.hash_password("test4")
            user.save_to_db()

            res = self.client.post("/login", data={"email": user.email, "password": "test4"})
            token = json.loads(res.data)["token"]

            res = self.client.get(f"/library/{user.email}", data={"library_type": "Potato"}, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(409, res.status_code)

    # TEST TASK 4
    def test_post_entry(self):
        with self.app.app_context():
            user = UsersModel("test", "test")
            user.hash_password("test")
            user.save_to_db()

            book = BooksModel(1, 1, 1, "test")
            book.save_to_db()

            res = self.client.post("/login", data={"email": user.email, "password": "test"})
            token = json.loads(res.data)["token"]

            parameters = {
                'isbn': book.isbn,
                'email': user.email
            }

            res = self.client.post("/library", data=parameters, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            self.assertEqual(LibraryModel.find_by_id_and_isbn(user.id, 1).json(), json.loads(res.data))

    def test_post_entry_without_login(self):
        with self.app.app_context():
            user = UsersModel("test", "test")
            user.hash_password("test2")
            user.save_to_db()

            res = self.client.post(f"/library")
            self.assertEqual(401, res.status_code)

    def test_post_entry_invalid_parameter(self):
        with self.app.app_context():
            user = UsersModel("test", "test")
            user.hash_password("test")
            user.save_to_db()

            res = self.client.post("/login", data={"email": user.email, "password": "test"})
            token = json.loads(res.data)["token"]

            parameters = {
                'isbn': 40,
                'email': user.email
            }

            res = self.client.post("/library", data=parameters, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(404, res.status_code)


if __name__ == '__main__':
    unittest.main()
