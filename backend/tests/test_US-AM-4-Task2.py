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


if __name__ == '__main__':
    unittest.main()
