import json

from model.books import BooksModel
from tests.base_test import BaseTest


class UnitTestOfUS(BaseTest):

    # TEST TASK 1
    def test_get_search_by_isbn(self):
        with self.app.app_context():
            book = BooksModel(9780553803716, 1, 1, "test")
            book.save_to_db()
            book = BooksModel(9780553803712, 1, 1, "test2")
            book.save_to_db()
            args = {
                "isbn": 9780553803716
            }
            res = self.client.get('/api/search', data=args)
            self.assertEqual(200, res.status_code)
            self.assertEqual(len(json.loads(res.data)["books"]), 1)
            list_books = list(map(lambda u: u.json(), BooksModel.query.filter_by(isbn=args['isbn']).all()))
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_search_by_autor(self):
        with self.app.app_context():
            book = BooksModel(1, 1, 1, "test", "Isaac Asimov")
            book.save_to_db()
            book = BooksModel(2, 1, 1, "as")
            book.save_to_db()
            args = {
                'autor': "Isaac Asimov"
            }
            res = self.client.get('/api/search', data=args)
            self.assertEqual(200, res.status_code)
            self.assertEqual(len(json.loads(res.data)["books"]), 1)
            list_books = list(map(lambda u: u.json(), BooksModel.query.filter_by(autor=args['autor']).all()))
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_search_by_title(self):
        with self.app.app_context():
            book = BooksModel(1, 1, 1, "test", "Isaac Asimov")
            book.save_to_db()
            book = BooksModel(2, 1, 1, "as")
            book.save_to_db()
            args = {
                'titulo': "test"
            }
            res = self.client.get('/api/search', data=args)
            self.assertEqual(200, res.status_code)
            self.assertEqual(len(json.loads(res.data)["books"]), 1)
            list_books = list(map(lambda u: u.json(), BooksModel.query.filter_by(titulo=args['titulo']).all()))
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_search_by_editorial(self):
        with self.app.app_context():
            book = BooksModel(1, 1, 1, "test", "Isaac Asimov", "Bantam Books")
            book.save_to_db()
            book = BooksModel(2, 1, 1, "as")
            book.save_to_db()
            args = {
                'editorial': "Bantam Books"
            }
            res = self.client.get('/api/search', data=args)
            self.assertEqual(200, res.status_code)
            self.assertEqual(len(json.loads(res.data)["books"]), 1)
            list_books = list(map(lambda u: u.json(), BooksModel.query.filter_by(editorial=args['editorial']).all()))
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_search_by_editorial_and_title(self):
        with self.app.app_context():
            book = BooksModel(1, 1, 1, "test", "Isaac Asimov", "Bantam Books")
            book.save_to_db()
            book = BooksModel(2, 1, 1, "as")
            book.save_to_db()
            args = {
                'titulo': "test",
                'editorial': "Bantam Books"
            }
            res = self.client.get('/api/search', data=args)
            self.assertEqual(200, res.status_code)
            self.assertEqual(len(json.loads(res.data)["books"]), 1)
            list_books = list(map(lambda u: u.json(), BooksModel.query.filter_by(editorial=args['editorial']).all()))
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_search_empty(self):
        with self.app.app_context():
            res = self.client.get('/api/search', data={})
            self.assertEqual(406, res.status_code)

    def test_get_search_empty_score_and_reviews (self):
        with self.app.app_context():
            args = {'score': True, 'reviews': True}
            res = self.client.get('/api/search', data=args)
            self.assertEqual(406, res.status_code)