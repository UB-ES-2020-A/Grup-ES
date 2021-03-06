import unittest
import json
import base64

from model.users import UsersModel
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):

    # TEST TASK 1
    def test_add(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'test@email.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)
            self.assertEqual(UsersModel.find_by_username('test').username, to_add.username)

    def test_add_same_username(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'test@email.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)

            to_add = UsersModel('test', 'test_not_same@email.com')
            to_add.hash_password('password')
            with self.assertRaises(Exception):
                UsersModel.save_to_db(to_add)

    def test_add_same_email(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'test@email.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)

            to_add = UsersModel('test_not_same', 'test@email.com')
            to_add.hash_password('password')
            with self.assertRaises(Exception):
                UsersModel.save_to_db(to_add)

    def test_delete_but_keep(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'test@email.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)

            UsersModel.delete_from_db(UsersModel.find_by_username('test'))
            keeps = len(UsersModel.query.filter_by(username='test', state=False).all())
            self.assertNotEqual(keeps, 0)

    # TEST TASK 2
    def test_post_user(self):
        with self.app.app_context():
            res = self.client.post("/api/user", data={"username": "test2", "email": "test2@email.com", "password": "Test1234"})
            self.assertEqual(201, res.status_code)
            self.assertEqual(UsersModel.find_by_username("test2").json(), json.loads(res.data))

            res = self.client.post("/api/user", data={"username": "test2", "email": "test2@email.com", "password": "Test1234"})
            self.assertEqual(409, res.status_code)

    # TEST TASK 3
    def test_login_user(self):
        with self.app.app_context():
            user = UsersModel("test3", "test3@email.com")
            user.hash_password("test3")
            user.save_to_db()

            res = self.client.post("/api/login", data={"email": "test3@email.com", "password": "test3"})
            self.assertEqual(200, res.status_code)
            self.assertEqual(user, UsersModel.verify_auth_token(json.loads(res.data)["token"]))

    # TEST NO TASK
    def test_get_user(self):
        with self.app.app_context():
            user = UsersModel("test", "test@email.com")
            user.hash_password("test")
            user.save_to_db()

            res = self.client.get("/api/user/test@email.com")
            self.assertEqual(200, res.status_code)
            self.assertEqual(user.json(), json.loads(res.data)["user"])

            res = self.client.get("/api/user/doesntexist")
            self.assertEqual(404, res.status_code)

    def test_delete_user(self):
        with self.app.app_context():
            user = UsersModel("test4", "test4@email.com")
            user.hash_password("test4")
            user.save_to_db()

            res = self.client.post("/api/login", data={"email": "test4@email.com", "password": "test4"})
            self.assertEqual(200, res.status_code)

            token = json.loads(res.data)["token"]
            res = self.client.delete("/api/user/test4@email.com", headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)

    def test_get_users(self):
        with self.app.app_context():
            user = UsersModel("test5", "test5@email.com")
            user.hash_password("test5")
            user.save_to_db()

            res = self.client.get("/api/users")
            self.assertEqual(200, res.status_code)
            list_users = list(map(lambda u: u.json(), UsersModel.query.all()))
            self.assertEqual(list_users, json.loads(res.data)["users"])


if __name__ == '__main__':
    unittest.main()
