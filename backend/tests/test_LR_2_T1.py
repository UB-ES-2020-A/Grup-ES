import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from db import db
from model.users import UsersModel


# Run from empty db
class TestBasicFunction(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['DEBUG'] = False
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test_data.db"
        self.client = self.app.test_client()

        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
            db.session.commit()

    def test_add(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'test@email.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)
            self.assertEqual(UsersModel.find_by_username('test').username, to_add.username)

    def test_add_same_username(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'test@email.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)

            to_add = UsersModel('test', 'test_not_same@email.com')
            to_add.hash_password('password')
            with self.assertRaises(Exception):
                UsersModel.save_to_db(to_add)

    def test_add_same_email(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'test@email.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)

            to_add = UsersModel('test_not_same', 'test@email.com')
            to_add.hash_password('password')
            with self.assertRaises(Exception):
                UsersModel.save_to_db(to_add)

    def test_delete_but_keep(self):
        with self.app.app_context():
            to_add = UsersModel('test', 'test@email.com')
            to_add.hash_password('password')
            UsersModel.save_to_db(to_add)

            UsersModel.delete_from_db(UsersModel.find_by_username('test'))
            keeps = len(UsersModel.query.filter_by(username='test', state=False).all())
            self.assertNotEqual(keeps, 0)


if __name__ == '__main__':
    unittest.main()
