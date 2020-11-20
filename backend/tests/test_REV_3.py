import base64
import json
import unittest

from tests.base_test import BaseTest
from model.reviews import ReviewsModel, ScoresModel
from model.books import BooksModel
from model.users import UsersModel


class UnitTestOfUS(BaseTest):

    @classmethod
    def dummy_book(cls):
        return BooksModel(1, 1, 1, "title")

    @classmethod
    def dummy_user(cls):
        user = UsersModel("username", "email@gmail.com")
        user.hash_password("p4ssw0rd!")
        return user

    @classmethod
    def login_dummy_user(cls, client):
        res = client.post("/login", data={"email": "email@gmail.com", "password": "p4ssw0rd!"})
        return json.loads(res.data)["token"]

    # TEST TASK 2
    def test_model_add_review(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            user = self.dummy_user()
            user.save_to_db()

            review = ReviewsModel(book.isbn, user.id, 5, "This is a extensive review of how this book is so good!")
            review.save_to_db()

            self.assertEqual(review, ReviewsModel.find_by_isbn_user_id(review.isbn, review.user_id))

    def test_model_add_review_duplicate(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            user = self.dummy_user()
            user.save_to_db()

            review = ReviewsModel(book.isbn, user.id, 5, "This is a extensive review of how this book is so good!")
            review.save_to_db()

            second_review = ReviewsModel(book.isbn, user.id, 5, "Omo! This book is so good I want to rate it twice.")
            with self.assertRaises(Exception):
                second_review.save_to_db()

    def test_model_add_review_of_non_existing_book(self):
        with self.app.app_context():
            user = self.dummy_user()
            user.save_to_db()

            review = ReviewsModel(1, user.id, 5, "This is a extensive review of how this book is so good!")
            with self.assertRaises(Exception):
                review.save_to_db()

    def test_model_add_review_of_non_existing_user(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            review = ReviewsModel(book.isbn, 1, 5, "This is a extensive review of how this book is so good!")
            with self.assertRaises(Exception):
                review.save_to_db()

    def test_model_add_review_with_wrong_score(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            user = self.dummy_user()
            user.save_to_db()

            with self.assertRaises(ValueError):
                ReviewsModel(book.isbn, user.id, 0, "Wow such book should not exist").save_to_db()
            with self.assertRaises(ValueError):
                ReviewsModel(book.isbn, user.id, -5, "Go to hell you BOOK!").save_to_db()
            with self.assertRaises(ValueError):
                ReviewsModel(book.isbn, user.id, 10, "This shit is like crack!").save_to_db()

    def test_model_score_add(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            user = self.dummy_user()
            user.save_to_db()

            review = ReviewsModel(book.isbn, user.id, 5, "This is a extensive review of how this book is so good!")

            ScoresModel.add_review(review)
            score = ScoresModel.find_by_isbn(review.isbn)
            self.assertEqual(review.score, score.score)

    def test_model_score_remove(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            user = self.dummy_user()
            user.save_to_db()

            review = ReviewsModel(book.isbn, user.id, 5, "This is a extensive review of how this book is so good!")

            ScoresModel.add_review(review)
            ScoresModel.remove_review(review)
            score = ScoresModel.find_by_isbn(review.isbn)
            self.assertIsNone(score)

    def test_model_score_remove_non_existing(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            user = self.dummy_user()
            user.save_to_db()

            review = ReviewsModel(book.isbn, user.id, 5, "This is a extensive review of how this book is so good!")

            with self.assertRaises(Exception):
                ScoresModel.remove_review(review)

    def test_model_score_remove_twice(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            user = self.dummy_user()
            user.save_to_db()

            review = ReviewsModel(book.isbn, user.id, 5, "This is a extensive review of how this book is so good!")

            ScoresModel.add_review(review)
            ScoresModel.remove_review(review)
            with self.assertRaises(Exception):
                ScoresModel.remove_review(review)

    # TEST TASK 3
    def test_post_review(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            user = self.dummy_user()
            user.save_to_db()

            token = self.login_dummy_user(self.client)

            parameters = {
                'isbn': book.isbn,
                'email': user.email,
                'score': 5,
                'review': "This book is good!"
            }

            res = self.client.post("/review", data=parameters, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(201, res.status_code)
            json.loads(res.data)
            self.assertEqual(ReviewsModel.find_by_isbn_user_id(book.isbn, user.id).json(), json.loads(res.data))

    def test_post_review_without_login(self):
        with self.app.app_context():
            user = self.dummy_user()
            user.save_to_db()

            book = self.dummy_book()
            book.save_to_db()

            res = self.client.post("/review")
            self.assertEqual(401, res.status_code)

    def test_post_review_non_existing_book(self):
        with self.app.app_context():
            user = self.dummy_user()
            user.save_to_db()

            token = self.login_dummy_user(self.client)

            parameters = {
                'isbn': 1,
                'email': user.email,
                'score': 5,
                'review': "This is a extensive review of how this book is so good!"
            }

            res = self.client.post("/review", data=parameters, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(404, res.status_code)

    def test_post_two_reviews_same_book(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            user = self.dummy_user()
            user.save_to_db()

            token = self.login_dummy_user(self.client)

            parameters = {
                'isbn': book.isbn,
                'email': user.email,
                'score': 5,
                'review': "This is a extensive review of how this book is so good!"
            }

            res = self.client.post("/review", data=parameters, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            res = self.client.post("/review", data=parameters, headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(500, res.status_code)


def test_post_review_wrong_score(self):
    with self.app.app_context():
        book = self.dummy_book()
        book.save_to_db()

        user = self.dummy_user()
        user.save_to_db()

        token = self.login_dummy_user(self.client)

        parameters = {
            'isbn': book.isbn,
            'email': user.email,
            'score': 0,
            'review': "Wow such book should not exist"
        }

        res = self.client.post("/review", data=parameters, headers={
            "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
        })
        self.assertEqual(418, res.status_code)




if __name__ == '__main__':
    unittest.main()
