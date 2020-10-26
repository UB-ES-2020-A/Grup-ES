import unittest
from flask import Flask
from db import db, secret_key
from flask_migrate import Migrate
from model.users import UsersModel


# Run from empty db
class TestBasicFunction(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test_data.db"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = secret_key

        migrate = Migrate(app, db)
        db.init_app(app)
        app.app_context().push()

    def test_add(self):
        to_add = UsersModel('test', 'test@email.com')
        to_add.hash_password('password')
        UsersModel.save_to_db(to_add)
        self.assertEqual(UsersModel.find_by_username('test').username, to_add.username)

    def test_add_same_username(self):
        to_add = UsersModel('test', 'test_not_same@email.com')
        to_add.hash_password('password')
        with self.assertRaises(Exception):
            UsersModel.save_to_db(to_add)

    def test_add_same_email(self):
        to_add = UsersModel('test_not_same', 'test@email.com')
        to_add.hash_password('password')
        with self.assertRaises(Exception):
            UsersModel.save_to_db(to_add)

    def test_delete_but_keep(self):
        UsersModel.delete_from_db(UsersModel.find_by_username('test'))
        keeps = len(UsersModel.query.filter_by(username='test', state=False).all())
        self.assertNotEqual(keeps, 0)


if __name__ == '__main__':
    unittest.main()
