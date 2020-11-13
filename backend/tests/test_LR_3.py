import json
import unittest

from model.users import UsersModel
from tests.base_test import BaseTest
from model.recovery import PasswordRecoveryModel


class UnitTestOfUS(BaseTest):

    # TASK 3
    def test_model_add(self):
        with self.app.app_context():
            recovery = PasswordRecoveryModel(1)
            recovery.save_to_db()

            self.assertEqual(PasswordRecoveryModel.find_by_id(recovery.user_id).json(), recovery.json())

    def test_model_add_duplicate_id(self):
        with self.app.app_context():
            recovery = PasswordRecoveryModel(1)
            recovery.save_to_db()

            same_recovery = PasswordRecoveryModel(1)
            with self.assertRaises(Exception):
                same_recovery.save_to_db()

    def test_model_add_duplicate_key(self):
        with self.app.app_context():
            recovery = PasswordRecoveryModel(1)
            recovery.save_to_db()

            same_recovery = PasswordRecoveryModel(2, key=recovery.key)
            with self.assertRaises(Exception):
                same_recovery.save_to_db()

    def test_model_delete(self):
        with self.app.app_context():
            recovery = PasswordRecoveryModel(1)
            recovery.save_to_db()

            recovery.delete_from_db()
            self.assertEqual([], PasswordRecoveryModel.query.all())

    # TASK 6
    def test_get_validation(self):
        with self.app.app_context():
            user = UsersModel("test", "test")
            user.hash_password("test")
            user.save_to_db()

            recovery = PasswordRecoveryModel(user.id)
            recovery.save_to_db()

            res = self.client.get(f"/recovery/check/{recovery.key}")
            self.assertEqual(200, res.status_code)
            self.assertEqual(UsersModel.find_by_id(user.id).json(), json.loads(res.data)["user"])

    def test_get_invalid_validation(self):
        with self.app.app_context():
            user = UsersModel("test2", "test2")
            user.hash_password("test2")
            user.save_to_db()

            res = self.client.get(f"/recovery/check/fails")
            self.assertEqual(404, res.status_code)
            self.assertEqual("PasswordRecovery with ['key':fails] is invalid", json.loads(res.data)["message"])


if __name__ == '__main__':
    unittest.main()
