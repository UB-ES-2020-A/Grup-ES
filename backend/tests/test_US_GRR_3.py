import base64
import json
import unittest

from tests.base_test import BaseTest
from model.users import UsersModel
from model.books import BooksModel
# Solves problem of user model not finding reviews model
from model.reviews import ReviewsModel


class UnitTestOfUS(BaseTest):

    def basic_setup(self):
        password = "test"
        self.user = UsersModel("test", "test")
        self.user.hash_password(password)
        self.user.save_to_db()

        self.book = BooksModel(1, 1, 1, "test")
        self.book.save_to_db()

        res = self.client.post("/login", data={"email": self.user.email, "password": password})
        self.token = json.loads(res.data)["token"]

    def test_delete_review(self):
        with self.app.app_context():
            self.basic_setup()

            review = ReviewsModel(self.book.isbn, self.user.id, 3, "test")
            review.save_to_db()

            res = self.client.delete(f"/review/{self.user.id}/{self.book.isbn}", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)
            self.assertEqual(None, ReviewsModel.find_by_isbn_user_id(self.book.isbn, self.user.id))

    def test_delete_review_other_user(self):
        with self.app.app_context():
            self.basic_setup()

            user2 = UsersModel("test2", "test2")
            user2.hash_password("test2")
            user2.save_to_db()

            review = ReviewsModel(self.book.isbn, user2.id, 3, "test")
            review.save_to_db()

            res = self.client.delete(f"/review/{user2.id}/{self.book.isbn}", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })

            self.assertEqual(401, res.status_code)
            # Checks not modified
            self.assertEqual(review, ReviewsModel.find_by_isbn_user_id(self.book.isbn, user2.id))

    def test_delete_review_not_created(self):
        with self.app.app_context():
            self.basic_setup()

            res = self.client.delete(f"/review/{self.user.id}/{self.book.isbn}", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(404, res.status_code)

    def test_delete_book_does_not_exist(self):
        with self.app.app_context():
            self.basic_setup()

            res = self.client.delete(f"/review/{self.user.id}/0", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(404, res.status_code)

    def test_delete_user_does_not_exist(self):
        with self.app.app_context():
            self.basic_setup()

            res = self.client.delete(f"/review/0/{self.book.isbn}", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(404, res.status_code)

    def test_delete_not_logged(self):
        with self.app.app_context():
            self.basic_setup()

            res = self.client.delete(f"/review/{self.user.id}/{self.book.isbn}")
            self.assertEqual(401, res.status_code)
