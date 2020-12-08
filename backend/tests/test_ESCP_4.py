import unittest
import json
from sqlalchemy import desc, asc

from model.books import BooksModel
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):

    # TEST TASK 1
    def test_get_book1(self):
        with self.app.app_context():
            book = BooksModel(1, 1, 1, "test")
            book.save_to_db()
            book = BooksModel(2, 1, 1, "as")
            book.save_to_db()
            args = {
                "numBooks": 2,
                "param": "isbn",
                "order": "desc"
            }
            res = self.client.get('/api/books', data=args)
            self.assertEqual(200, res.status_code)
            list_books = list(map(lambda u: u.json(), BooksModel.query.order_by(desc('isbn')).limit(2).all()))
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_books(self):
        with self.app.app_context():
            book = BooksModel(1, 1, 1, "test")
            book.save_to_db()
            book = BooksModel(2, 1, 1, "as")
            book.save_to_db()
            res = self.client.get('/api/books')
            self.assertEqual(200, res.status_code)
            list_books = list(map(lambda u: u.json(), BooksModel.query.all()))
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_book2(self):
        with self.app.app_context():
            book1 = BooksModel(1, 1, 1, "aaaa")
            book1.save_to_db()
            book2 = BooksModel(2, 1, 1, "bbbb")
            book2.save_to_db()
            book2.vendible = False
            args = {
                "numBooks": 2,
                "param": "titulo",
                "order": "asc"
            }
            res = self.client.get('/api/books', data=args)
            self.assertEqual(200, res.status_code)
            list_books = list(map(lambda u: u.json(), BooksModel.query.filter_by(vendible=True).order_by(asc('titulo')).limit(2).all()))
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_new_releases(self):
        with self.app.app_context():
            book1 = BooksModel(1, 1, 1, "aaaa")
            book1.save_to_db()
            book2 = BooksModel(2, 1, 1, "bbbb")
            book2.save_to_db()
            args = {
                "param": "fecha_de_publicacion",
                "order": "desc"
            }
            res = self.client.get('/api/books', data=args)
            self.assertEqual(200, res.status_code)
            list_books = list(map(lambda u: u.json(), BooksModel.query.filter_by(vendible=True).order_by(desc('fecha_de_publicacion')).all()))
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_new_releases_vendible_false(self):
        with self.app.app_context():
            book1 = BooksModel(1, 1, 1, "aaaa")
            book1.save_to_db()
            book2 = BooksModel(2, 1, 1, "bbbb")
            book2.save_to_db()
            book2.vendible = False
            args = {
                "param": "fecha_de_publicacion",
                "order": "desc"
            }
            res = self.client.get('/api/books', data=args)
            self.assertEqual(200, res.status_code)
            list_books = list(map(lambda u: u.json(), BooksModel.query.filter_by(vendible=True).
                                  order_by(desc('fecha_de_publicacion')).all()))
            self.assertEqual(1, len(json.loads(res.data)["books"]))
            self.assertEqual(list_books, json.loads(res.data)["books"])

    # TEST TASK 2
    def test_get_book(self):
        with self.app.app_context():
            book = BooksModel(1, 1, 1, "test")
            book.save_to_db()

            res = self.client.get("/api/book/1")
            self.assertEqual(200, res.status_code)
            self.assertEqual(book.json(), json.loads(res.data)["book"])

    def test_get_invalid_book(self):
        with self.app.app_context():
            res = self.client.get("/api/book/1")
            self.assertEqual(404, res.status_code)


if __name__ == '__main__':
    unittest.main()
