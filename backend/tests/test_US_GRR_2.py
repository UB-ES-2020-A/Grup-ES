import base64
import json

from tests.base_test import BaseTest
from model.users import UsersModel
from model.books import BooksModel
# Solves problem of user model not finding reviews model
from model.reviews import ReviewsModel, ScoresModel


class UnitTestOfUS(BaseTest):

    def basic_setup(self):
        password = "test"
        self.user = UsersModel("test", "test")
        self.user.hash_password(password)
        self.user.save_to_db()

        self.book = BooksModel(1, 1, 1, "test")
        self.book.save_to_db()

        res = self.client.post("/api/login", data={"email": self.user.email, "password": password})
        self.token = json.loads(res.data)["token"]

    def test_model_update_one_score(self):
        with self.app.app_context():
            self.basic_setup()

            review = ReviewsModel(self.book.isbn, self.user.id, 2)
            review.save_to_db()

            data = {"score": 3}
            review.update_from_db(data)

            self.assertEqual(data["score"], review.score)
            self.assertEqual(data["score"], ScoresModel.find_by_isbn(self.book.isbn).score)

    def test_model_update_several_score(self):
        with self.app.app_context():
            self.basic_setup()

            user2 = UsersModel("test2", "test2")
            user2.hash_password("test2")
            user2.save_to_db()

            review = ReviewsModel(self.book.isbn, self.user.id, 2)
            review.save_to_db()

            review2 = ReviewsModel(self.book.isbn, user2.id, 4)
            review2.save_to_db()

            data = {"score": 3}
            review.update_from_db(data)

            self.assertEqual(data["score"], review.score)
            self.assertEqual((data["score"] + review2.score)/2, ScoresModel.find_by_isbn(self.book.isbn).score)

    def test_model_update_all_parameters(self):
        with self.app.app_context():
            self.basic_setup()

            review = ReviewsModel(self.book.isbn, self.user.id, 2)
            review.save_to_db()

            data = {"score": 3, "review": "test review"}
            review.update_from_db(data)

            # Checks all items have been updated
            self.assertDictEqual(data, {k: v for k, v in review.json().items() if k in data})
            self.assertEqual(data["score"], ScoresModel.find_by_isbn(self.book.isbn).score)

    def test_update_review(self):
        with self.app.app_context():
            self.basic_setup()

            review = ReviewsModel(self.book.isbn, self.user.id, 3, "test")
            review.save_to_db()

            data = {"score": 1, "review": "test review"}
            res = self.client.put(f"/api/review/{self.user.id}/{self.book.isbn}", data=data, headers={
                "Authorization": 'Basic ' + base64.b64encode((self.token + ":").encode('ascii')).decode('ascii')
            })

            self.assertEqual(200, res.status_code)
            # Checks all items have been updated
            self.assertDictEqual(data, {k: v for k, v in json.loads(res.data)["review"].items() if k in data})

# All exit cases are checked at the test of US-GRR-1-Task2
