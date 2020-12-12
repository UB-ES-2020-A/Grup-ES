from model.users import UsersModel
from model.verify_email import VerifyModel
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):
    def basic_setup(self):
        self.user = UsersModel('test2', 'bookshelterES@gmail.com')
        self.user.hash_password('Test1234')
        UsersModel.save_to_db(self.user)
        self.user = UsersModel.find_by_username("test2")
        self.verify = VerifyModel(self.user.id)
        self.verify.save_to_db()
        url_root = 'www.test.com/'
        self.verify.send_email(self.user.email, url_root)

    def basic_user(self):
        self.user = UsersModel('test2', 'bookshelterES@gmail.com')
        self.user.hash_password('Test1234')
        UsersModel.save_to_db(self.user)

    # TEST TASK 2
    def test_model_add(self):
        with self.app.app_context():
            self.basic_user()
            verify_entry = VerifyModel(self.user.id)

            verify_entry.save_to_db()
            self.assertEqual(verify_entry, VerifyModel.find_by_id(self.user.id))

    def test_model_add_duplicate(self):
        with self.app.app_context():
            self.basic_user()
            verify_entry = VerifyModel(self.user.id)

            verify_entry.save_to_db()
            self.assertEqual(verify_entry, VerifyModel.find_by_id(self.user.id))

            same_verify_entry = VerifyModel(self.user.id)
            with self.assertRaises(Exception):
                same_verify_entry.save_to_db()

    def test_model_delete(self):
        with self.app.app_context():
            self.basic_user()
            verify_entry = VerifyModel(self.user.id)

            verify_entry.save_to_db()
            self.assertEqual(verify_entry, VerifyModel.find_by_id(self.user.id))
            verify_entry.delete_from_db()
            self.assertEqual(None, VerifyModel.find_by_id(self.user.id))

    def test_verify_user(self):
        with self.app.app_context():
            self.basic_setup()
            self.assertEqual(self.user.confirmed_email.confirmed_email, False)
            res = self.client.post(f"/api/verify/{self.verify.key}")
            self.assertEqual(self.user.confirmed_email.confirmed_email, True)

    def test_verify_user_wrong_key(self):
        with self.app.app_context():
            self.basic_setup()

            self.assertEqual(self.user.confirmed_email.confirmed_email, False)
            res = self.client.post(f"/api/verify/{'wrong_key'}")
            self.assertEqual(404, res.status_code)
            self.assertEqual(self.user.confirmed_email.confirmed_email, False)

    def test_verify_user_expired_key(self):
        with self.app.app_context():
            self.basic_setup()

            self.assertEqual(self.user.confirmed_email.confirmed_email, False)
            self.verify.time -= 2 * self.verify.VALID_UNTIL
            res = self.client.post(f"/api/verify/{self.verify.key}")
            self.assertEqual(404, res.status_code) # mai surt 403 perque netejem les claus expirades
            self.assertEqual(self.user.confirmed_email.confirmed_email, False)
