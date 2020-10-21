from flask import g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context

from db import db, secret_key
import datetime as dt

ROLES = ['manager','user']
auth = HTTPBasicAuth()

class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.Enum(*ROLES), nullable=False)
    state = db.Column(db.Boolean(), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    def __init__(self, username, email, role='user'):
        self.username = username
        self.email = email
        self.role = role
        self.state = True
        self.date = dt.datetime.today()

    def __repr__(self):
        return f"<{self.username}-{self.email}-{self.role}-{self.date}>"

    def save_to_db(self):
        if 0 < self.query.filter_by(username=self.username, state=True).count():
            raise Exception("Username already in use")
        elif 0 < self.query.filter_by(email=self.email, state=True).count():
            raise Exception("Email already in use")
        else:
            db.session.add(self)
            db.session.commit()

    def json(self):
        return {"username": self.username,
                "email": self.email,
                "role": self.role}

    def delete_from_db(self):
        self.state = False
        db.session.commit()

    def verify_password(self, password):
        return password == self.password

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username, state=True).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email, state=True).first()

    @classmethod
    def return_all(cls):
        return cls.query.all()

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'username': self.username})

    @classmethod
    def verify_auth_token(cls, token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = cls.query.filter_by(username=data['username'], state=True).first()
        return user

    @auth.verify_password
    def verify_password(token, password):
        user = UsersModel.verify_auth_token(token)
        if user:
            g.user = user
            return user

    @auth.get_user_roles
    def get_user_roles(user):
        return user.role
