import unittest
import json
from sqlalchemy import desc, asc

from model.books import BooksModel
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):

    def init_books(self):
        self.book = BooksModel(1, 1, 1, "test")
        self.book.save_to_db()
        self.book2 = BooksModel(2, 1, 1, "as")
        self.book2.save_to_db()

    # TEST TASK 1
    def test_get_book1(self):
        with self.app.app_context():
            self.init_books()
            args = {
                "numBooks": 2,
                "param": "isbn",
                "order": "desc"
            }
            res = self.client.get('/api/books', data=args)
            self.assertEqual(200, res.status_code)
            list_books = [book.json() for book in BooksModel.query.order_by(desc('isbn')).limit(2).all()]
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_books(self):
        with self.app.app_context():
            self.init_books()
            res = self.client.get('/api/books')
            self.assertEqual(200, res.status_code)
            list_books = [book.json() for book in BooksModel.query.all()]
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_book2(self):
        with self.app.app_context():
            self.init_books()
            self.book2.update_from_db({"vendible": False})

            args = {
                "numBooks": 2,
                "param": "titulo",
                "order": "asc"
            }
            res = self.client.get('/api/books', data=args)
            self.assertEqual(200, res.status_code)
            list_books = [book.json() for book in
                          BooksModel.query.filter_by(vendible=True).order_by(asc('titulo')).limit(2).all()]
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_book3(self):
        with self.app.app_context():
            self.init_books()
            self.book2.update_from_db({"vendible": False})

            args = {
                "showOnlyVendibles": True
            }
            res = self.client.get('/api/books', data=args)
            self.assertEqual(200, res.status_code)
            list_books = [book.json() for book in BooksModel.query.filter_by(vendible=True).all()]
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_books_all(self):
        with self.app.app_context():
            self.init_books()
            self.book2.update_from_db({"vendible": False})

            args = {
                "showOnlyVendibles": False
            }
            res = self.client.get('/api/books', data=args)
            self.assertEqual(200, res.status_code)
            list_books = [book.json() for book in BooksModel.query.all()]
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_new_releases(self):
        with self.app.app_context():
            self.init_books()

            args = {
                "param": "fecha_de_publicacion",
                "order": "desc"
            }
            res = self.client.get('/api/books', data=args)
            self.assertEqual(200, res.status_code)
            list_books = [book.json() for book in
                          BooksModel.query.filter_by(vendible=True).order_by(desc('fecha_de_publicacion')).all()]
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_new_releases_vendibles(self):
        with self.app.app_context():
            self.init_books()
            self.book2.update_from_db({"vendible": False})

            args = {
                "param": "fecha_de_publicacion",
                "order": "desc",
                "showOnlyVendibles": True
            }
            res = self.client.get('/api/books', data=args)
            self.assertEqual(200, res.status_code)
            list_books = [book.json() for book in
                          BooksModel.query.filter_by(vendible=True).order_by(desc('fecha_de_publicacion')).all()]
            self.assertEqual(1, len(json.loads(res.data)["books"]))
            self.assertEqual(list_books, json.loads(res.data)["books"])

    # TEST TASK 2
    def test_get_book(self):
        with self.app.app_context():
            self.init_books()

            res = self.client.get(f"/api/book/{self.book.isbn}")
            self.assertEqual(200, res.status_code)
            self.assertEqual(self.book.json(), json.loads(res.data)["book"])

    def test_get_invalid_book(self):
        with self.app.app_context():
            res = self.client.get("/api/book/0")
            self.assertEqual(404, res.status_code)


if __name__ == '__main__':
    unittest.main()
