import unittest
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
import json
from datetime import datetime

from model.books import BooksModel
from db import db
from resources.books import Books


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

        api.add_resource(Books, '/books')

        db.init_app(self.app)
        migrate = Migrate(self.app, db)

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
            db.session.commit()

    def test_get_book(self):
        with self.app.app_context():
            book = BooksModel(1, 1, 1, "test")
            book.save_to_db()

            #fins aqui bé, i després?

            res = self.client.get('/book')

