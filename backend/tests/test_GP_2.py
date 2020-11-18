import base64
import unittest
import json
from model.users import UsersModel
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):

    # TEST TASK 2
    def test_modify_username(self):
        with self.app.app_context():
            user = UsersModel("test", "test@gmail.com")
            user.hash_password("test")
            user.save_to_db()

            res = self.client.post("/login", data={"email": user.email, "password": "test"})
            token = json.loads(res.data)["token"]

            data_new = {
                'username': 'francina',
                'password': 'test',
                'email': 'test@gmail.com'
            }
            res = self.client.put(f"/user/{user.email}", data=data_new, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(data_new['username'], UsersModel.find_by_email(user.email).username)
