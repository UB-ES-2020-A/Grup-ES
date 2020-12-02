import base64
import json

from tests.base_test import BaseTest
from model.users import UsersModel, Roles
from model.books import BooksModel
from model.reviews import ReviewsModel


class UnitTestOfUS(BaseTest):

    def basic_setup(self):
        password = "admin"
        self.admin = UsersModel("admin", "admin", Roles.Admin)
        self.admin.hash_password(password)
        self.admin.save_to_db()

        self.user = UsersModel("test", "test")
        self.user.hash_password("test")
        self.user.save_to_db()

        self.book = BooksModel(2, 2, 2, "test")
        self.book.save_to_db()

        res = self.client.post("/login", data={"email": self.admin.email, "password": password})
        self.token = json.loads(res.data)["token"]

    def test_delete_review_admin(self):
        with self.app.app_context():
            self.basic_setup()

            review = ReviewsModel(self.book.isbn, self.user.id, 2, "test")
            review.save_to_db()

            res = self.client.delete(f"/review/{self.user.id}/{self.book.isbn}", headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)
            self.assertEqual(None, ReviewsModel.find_by_isbn_user_id(self.book.isbn, self.user.id))

    # All exit cases are checked at the test of US-GRR-1-Task2
