import base64
import unittest
import json

from model.books import BooksModel
from model.users import UsersModel
from tests.base_test import BaseTest
from model.transactions import TransactionsModel


class UnitTestOfUS(BaseTest):

# TEST TASK 1
    def test_get_search_by_isbn(self):
        with self.app.app_context():
            book = BooksModel(1, 1, 1, "test")
            book.save_to_db()
            book = BooksModel(2, 1, 1, "as")
            book.save_to_db()
            args = {
                "isbn": 1,
                'autor': "patata"
            }
            res = self.client.get('/search', data=args)
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
            res = self.client.get('/search', data=args)
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
                'titulo': "test",
                'editorial': 'no_importa'
            }
            res = self.client.get('/search', data=args)
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
            res = self.client.get('/search', data=args)
            self.assertEqual(200, res.status_code)
            self.assertEqual(len(json.loads(res.data)["books"]), 1)
            list_books = list(map(lambda u: u.json(), BooksModel.query.filter_by(editorial=args['editorial']).all()))
            self.assertEqual(list_books, json.loads(res.data)["books"])
