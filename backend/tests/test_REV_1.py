import json
import unittest

from tests.base_test import BaseTest
from model.reviews import ReviewsModel
from model.books import BooksModel
from model.users import UsersModel


class UnitTestOfUS(BaseTest):

    @classmethod
    def dummy_book(cls):
        return BooksModel(9780553803716, 1, 1, "title")

    @classmethod
    def dummy_user(cls):
        user = UsersModel("username", "email@gmail.com")
        user.hash_password("p4ssw0rd!")
        return user

    @classmethod
    def dummy_review(cls):
        return ReviewsModel(9780553803716, 1, 5, "This book is so good!")

    # TEST TASK 3
    def test_get_book_reviews(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            user = self.dummy_user()
            user.save_to_db()

            review = self.dummy_review()
            review.save_to_db()

            res = self.client.get(f"/api/book/{book.isbn}", data={'reviews': True, 'score': True})
            self.assertEqual(book.json(reviews=True, score=True), json.loads(res.data)["book"])

    def test_get_books_reviews(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            user = self.dummy_user()
            user.save_to_db()

            review = self.dummy_review()
            review.save_to_db()

            res = self.client.get(f"/api/books", data={'reviews': True, 'score': True})
            self.assertEqual(book.json(reviews=True, score=True), json.loads(res.data)["books"][0])

    def test_get_search_by_isbn_reviews(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            user = self.dummy_user()
            user.save_to_db()

            review = self.dummy_review()
            review.save_to_db()

            res = self.client.get(f"/api/search", data={"isbn": 9780553803716, 'reviews': True, 'score': True})
            self.assertEqual(book.json(reviews=True, score=True), json.loads(res.data)["books"][0])

    def test_get_user_reviews(self):
        with self.app.app_context():
            book = self.dummy_book()
            book.save_to_db()

            user = self.dummy_user()
            user.save_to_db()

            review = self.dummy_review()
            review.save_to_db()

            res = self.client.get(f"/api/user/{user.email}", data={"isbn": 1, 'reviews': True, 'score': True})
            self.assertEqual(user.json(reviews=True), json.loads(res.data)["user"])


if __name__ == '__main__':
    unittest.main()
