import base64
import json
from model.users import UsersModel
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):
    def basic_setup(self):
        self.user = UsersModel("test123", "test@gmail.com")
        self.user.hash_password("Test1234")
        self.user.save_to_db()

        res = self.client.post("/api/login", data={"email": self.user.email, "password": "Test1234"})
        self.token = json.loads(res.data)["token"]

    # TEST TASK 2
    def test_modify_username(self):
        with self.app.app_context():
            self.basic_setup()

            data_new = {
                'username': 'francina',
                'password': 'Test1234'
            }
            res = self.client.put(f"/api/user/{self.user.email}", data=data_new, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)
            self.assertEqual(data_new['username'], (json.loads(res.data)["user"])['username'])

    def test_modify_email(self):
        with self.app.app_context():
            self.basic_setup()
            data_new = {
                'email': 'francina@gmail.com',
                'password': 'Test1234'
            }
            res = self.client.put(f"/api/user/{self.user.email}", data=data_new, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)
            self.assertEqual(data_new['email'], (json.loads(res.data)["user"])['email'])

    def test_modify_username_already_used(self):
        with self.app.app_context():
            self.basic_setup()
            user2 = UsersModel("patata", "patata@gmail.com")
            user2.hash_password("patata")
            user2.save_to_db()

            data_new = {
                'username': user2.username,
                'password': 'Test1234'
            }
            res = self.client.put(f"/api/user/{self.user.email}", data=data_new, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(409, res.status_code)

    def test_modify_email_already_used(self):
        with self.app.app_context():
            self.basic_setup()
            user2 = UsersModel("patata", "patata@gmail.com")
            user2.hash_password("patata")
            user2.save_to_db()

            data_new = {
                'email': user2.email,
                'password': 'Test1234'
            }
            res = self.client.put(f"/api/user/{self.user.email}", data=data_new, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(409, res.status_code)

    def test_modify_password(self):
        with self.app.app_context():
            self.basic_setup()

            data_new = {
                'new_password': 'newTest1234',
                'password': 'Test1234'
            }
            res = self.client.put(f"/api/user/{self.user.email}", data=data_new, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)
            self.assertTrue(UsersModel.find_by_username('test123').check_password(data_new['new_password']))

    def test_modify_wrong_password(self):
        with self.app.app_context():
            self.basic_setup()

            data_new = {
                'username': 'asdfassa',
                'password': 'Wrong1234'
            }
            res = self.client.put(f"/api/user/{self.user.email}", data=data_new, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(401, res.status_code)

    def test_modify_without_login(self):
        with self.app.app_context():
            user = UsersModel("test", "test@gmail.com")
            user.hash_password("test")
            user.save_to_db()

            data_new = {
                'username': 'asdf',
                'password': 'wrong'
            }
            res = self.client.put(f"/api/user/{user.email}", data=data_new)
            self.assertEqual(401, res.status_code)
