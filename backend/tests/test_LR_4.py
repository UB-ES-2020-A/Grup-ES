from flask import request

from model.users import UsersModel
from model.verify_email import VerifyModel
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):

    # TEST TASK 2
    def test_verify_user(self):
        with self.app.app_context():

            user = UsersModel('test2', 'bookshelterES@gmail.com')
            user.hash_password('Test1234')
            UsersModel.save_to_db(user)
            user = UsersModel.find_by_username("test2")
            verify = VerifyModel(user.id)
            verify.save_to_db()
            url_root = 'www.test.com/'
            verify.send_email(user.email, url_root)

            self.assertEqual(user.confirmed_email.confirmed_email, False)
            res = self.client.post(f"/api/verify/{verify.key}")
            self.assertEqual(user.confirmed_email.confirmed_email, True)

    def test_verify_user_wrong_key(self):
        with self.app.app_context():

            user = UsersModel('test2', 'bookshelterES@gmail.com')
            user.hash_password('Test1234')
            UsersModel.save_to_db(user)
            user = UsersModel.find_by_username("test2")
            verify = VerifyModel(user.id)
            verify.save_to_db()
            url_root = 'www.test.com/'
            verify.send_email(user.email, url_root)

            self.assertEqual(user.confirmed_email.confirmed_email, False)
            res = self.client.post(f"/api/verify/{'wrong_key'}")
            self.assertEqual(404, res.status_code)
            self.assertEqual(user.confirmed_email.confirmed_email, False)

    def test_verify_user_expired_key(self):
        with self.app.app_context():
            user = UsersModel('test2', 'bookshelterES@gmail.com')
            user.hash_password('Test1234')
            UsersModel.save_to_db(user)
            user = UsersModel.find_by_username("test2")
            verify = VerifyModel(user.id)
            verify.save_to_db()
            url_root = 'www.test.com/'
            verify.send_email(user.email, url_root)

            self.assertEqual(user.confirmed_email.confirmed_email, False)
            verify.time -= 2 * verify.VALID_UNTIL
            res = self.client.post(f"/api/verify/{verify.key}")
            self.assertEqual(404, res.status_code) # mai surt 403 perque netejem les claus expirades
            self.assertEqual(user.confirmed_email.confirmed_email, False)
