import unittest
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
import json
from datetime import datetime

from sqlalchemy import asc, desc

from model.books import BooksModel
from db import db
from resources.books import Books, BooksList


class TestBasicFunction(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['DEBUG'] = False
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test_data.db"
        self.client = self.app.test_client()
        api = Api(self.app)

        api.add_resource(BooksList, '/books')

        db.init_app(self.app)
        migrate = Migrate(self.app, db)

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
            db.session.commit()

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
            res = self.client.get('/books', data=args)
            self.assertEqual(200, res.status_code)
            list_books = list(map(lambda u: u.json(), BooksModel.query.order_by(desc('isbn')).limit(2).all()))
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_books(self):
        with self.app.app_context():
            book = BooksModel(1, 1, 1, "test")
            book.save_to_db()
            book = BooksModel(2, 1, 1, "as")
            book.save_to_db()
            res = self.client.get('/books')
            self.assertEqual(200, res.status_code)
            list_books = list(map(lambda u: u.json(), BooksModel.query.all()))
            self.assertEqual(list_books, json.loads(res.data)["books"])

    def test_get_book2(self):
        with self.app.app_context():
            book = BooksModel(1, 1, 1, "aaaa")
            book.save_to_db()
            book = BooksModel(2, 1, 1, "bbbb")
            book.save_to_db()
            args = {
                "numBooks": 2,
                "param": "titulo",
                "order": "asc"
            }
            res = self.client.get('/books', data=args)
            self.assertEqual(200, res.status_code)
            list_books = list(map(lambda u: u.json(), BooksModel.query.order_by(asc('titulo')).limit(2).all()))
            self.assertEqual(list_books, json.loads(res.data)["books"])
