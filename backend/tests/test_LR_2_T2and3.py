import unittest
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from flask_restful import Api
import json
import base64

from model.users import UsersModel
from db import db
from resources.users import Users, UsersList, Login


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

        api.add_resource(Users, '/user/<string:email>', '/user')
        api.add_resource(UsersList, '/users')
        api.add_resource(Login, '/login')

        db.init_app(self.app)
        migrate = Migrate(self.app, db)

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
            db.session.commit()

    def test_get_user(self):
        with self.app.app_context():
            user = UsersModel("test", "test@email.com")
            user.hash_password("test")
            user.save_to_db()

            res = self.client.get("/user/test@email.com")
            self.assertEqual(200, res.status_code)
            self.assertEqual(user.json(), json.loads(res.data)["user"])

            res = self.client.get("/user/doesntexist")
            self.assertEqual(404, res.status_code)

    def test_post_user(self):
        with self.app.app_context():
            res = self.client.post("/user", data={"username": "test2", "email": "test2@email.com", "password": "test2"})
            self.assertEqual(201, res.status_code)
            self.assertEqual(UsersModel.find_by_username("test2").json(), json.loads(res.data))

            res = self.client.post("/user", data={"username": "test2", "email": "test2@email.com", "password": "test2"})
            self.assertEqual(409, res.status_code)

    def test_login_user(self):
        with self.app.app_context():
            user = UsersModel("test3", "test3@email.com")
            user.hash_password("test3")
            user.save_to_db()

            res = self.client.post("/login", data={"email": "test3@email.com", "password": "test3"})
            self.assertEqual(200, res.status_code)
            self.assertEqual(user, UsersModel.verify_auth_token(json.loads(res.data)["token"]))

    def test_delete_user(self):
        with self.app.app_context():
            user = UsersModel("test4", "test4@email.com")
            user.hash_password("test4")
            user.save_to_db()

            res = self.client.post("/login", data={"email": "test4@email.com", "password": "test4"})
            self.assertEqual(200, res.status_code)

            token = json.loads(res.data)["token"]
            res = self.client.delete("/user/test4@email.com", headers={
                "Authorization": 'Basic ' + base64.b64encode((token + ":").encode('ascii')).decode('ascii')
            })
            self.assertEqual(200, res.status_code)

    def test_get_users(self):
        with self.app.app_context():
            user = UsersModel("test5", "test5@email.com")
            user.hash_password("test5")
            user.save_to_db()

            res = self.client.get("/users")
            self.assertEqual(200, res.status_code)
            list_users = list(map(lambda u: u.json(), UsersModel.query.all()))
            self.assertEqual(list_users, json.loads(res.data)["users"])


if __name__ == '__main__':
    unittest.main()
