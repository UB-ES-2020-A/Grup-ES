import base64
import json
import unittest

from model.users import UsersModel
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):
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

            # veiem que s'esborra correctament
            self.assertEqual(200, res.status_code)
            res = self.client.get("/api/users")
            self.assertEqual(200, res.status_code)
            self.assertEqual(None, json.loads(res.data)["users"])

            # tornem a crear un usuari amb les mateixes dades i ens deixa
            user = UsersModel("test4", "test4@email.com")
            user.hash_password("test4")
            user.save_to_db()

            res = self.client.post("/api/login", data={"email": "test4@email.com", "password": "test4"})
            self.assertEqual(200, res.status_code)


if __name__ == '__main__':
    unittest.main()
