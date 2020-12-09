import json
import unittest

from model.users import UsersModel
from tests.base_test import BaseTest
from model.recovery import PasswordRecoveryModel
from utils.mail import mail


class UnitTestOfUS(BaseTest):

    # TASK 2
    def test_recovery_mail(self):
        with self.app.app_context(), mail.record_messages() as outbox:
            user = UsersModel("test", "test@gmail.com")
            user.hash_password("test")
            user.save_to_db()

            recovery = PasswordRecoveryModel(user.id)
            recovery.save_to_db()
            root = "http://test.com/"
            recovery.send_email(user.email, root)

            self.assertEqual(1, len(outbox))
            self.assertEqual("Password recovery", outbox[0].subject)
            self.assertEqual(user.email, outbox[0].recipients[0])
            self.assertTrue(f"http://test.com/reset?key={recovery.key}" in outbox[0].body)

    def test_post_recovery(self):
        with self.app.app_context(), mail.record_messages() as outbox:
            user = UsersModel("test", "test2@gmail.com")
            user.hash_password("test")
            user.save_to_db()

            res = self.client.post(f"/api/recovery", data={"email": user.email})
            self.assertEqual(201, res.status_code)
            self.assertEqual(1, len(outbox))
            self.assertEqual(PasswordRecoveryModel.find_by_id(user.id).json(), json.loads(res.data)["recovery"])

    def test_post_inavlid_recovery(self):
        with self.app.app_context(), mail.record_messages() as outbox:

            res = self.client.post(f"/api/recovery", data={"email": "fails"})
            self.assertEqual(404, res.status_code)
            self.assertEqual(0, len(outbox))

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

    # TASK 5
    def test_put_recovery(self):
        with self.app.app_context():
            user = UsersModel("test", "test")
            user.hash_password("test")
            user.save_to_db()

            recovery = PasswordRecoveryModel(user.id)
            recovery.save_to_db()

            new_password = "Test1234"
            res = self.client.put(f"/api/recovery/{recovery.key}", data={"new_password": new_password})
            self.assertEqual(200, res.status_code)
            self.assertEqual(user.json(), json.loads(res.data)["user"])
            self.assertTrue(user.check_password(new_password))

    def test_put_recovery_not_requested(self):
        with self.app.app_context():
            user = UsersModel("test", "test")
            user.hash_password("test")
            user.save_to_db()

            new_password = "Test1234"
            res = self.client.put(f"/api/recovery/notImportant", data={"new_password": new_password})
            self.assertEqual(403, res.status_code)

    def test_put_recovery_expired(self):
        with self.app.app_context():
            user = UsersModel("test", "test")
            user.hash_password("test")
            user.save_to_db()

            recovery = PasswordRecoveryModel(user.id)
            recovery.time -= 2 * PasswordRecoveryModel.VALID_UNTIL
            recovery.save_to_db()

            new_password = "Test1234"
            res = self.client.put(f"/api/recovery/{recovery.key}", data={"new_password": new_password})
            self.assertEqual(403, res.status_code)

    # TASK 6
    def test_get_validation(self):
        with self.app.app_context():
            user = UsersModel("test", "test")
            user.hash_password("test")
            user.save_to_db()

            recovery = PasswordRecoveryModel(user.id)
            recovery.save_to_db()

            res = self.client.get(f"/api/recovery/{recovery.key}")
            self.assertEqual(200, res.status_code)
            self.assertEqual(UsersModel.find_by_id(user.id).json(), json.loads(res.data)["user"])

    def test_get_invalid_validation(self):
        with self.app.app_context():
            user = UsersModel("test2", "test2")
            user.hash_password("test2")
            user.save_to_db()

            res = self.client.get(f"/api/recovery/fails")
            self.assertEqual(404, res.status_code)
            self.assertEqual("Password Recovery with ['key':fails] is invalid", json.loads(res.data)["message"])


if __name__ == '__main__':
    unittest.main()
