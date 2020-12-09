import unittest
import json
import base64

from model.users import UsersModel
from model.verify_email import VerifyModel
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):

    # TEST TASK 2
    def test_post_user(self):
        with self.app.app_context():
            res = self.client.post("/api/user", data={"username": "test2", "email": "bookshelterES@gmail.com", "password": "Test1234"})
            self.assertEqual(201, res.status_code)
            user = UsersModel.find_by_username("test2")
            self.assertEqual(user.json(), json.loads(res.data))

            self.assertEqual(user.confirmed_email, False)
            verify_key = VerifyModel.find_by_id(user.id)
            res = self.client.get(f"/api/verify/{verify_key.key}")
            self.assertEqual(user.confirmed_email, True)
