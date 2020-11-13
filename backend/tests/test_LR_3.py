import unittest

from tests.base_test import BaseTest
from model.recovery import PasswordRecoveryModel


class UnitTestOfUS(BaseTest):

    # TASK 3
    def test_model_add(self):
        with self.app.app_context():
            recovery = PasswordRecoveryModel(1)
            recovery.save_to_db()

            self.assertEqual(PasswordRecoveryModel.find_by_id(recovery.user_id), recovery)

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


if __name__ == '__main__':
    unittest.main()
