from flask import g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context
import datetime as dt
from enum import Enum


from db import db, secret_key

auth = HTTPBasicAuth()


class Roles(Enum):
    User = 1
    Admin = 2

    def __str__(self):
        return self.name


class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.Enum(Roles, name='roles_types'), nullable=False)
    state = db.Column(db.Boolean(), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    library = db.relationship('LibraryModel', backref='library', lazy=True)
    reviews = db.relationship('ReviewsModel', backref='user', lazy=True)
    transactions = db.relationship('TransactionsModel', backref='transactions', lazy=True)

    def __init__(self, username, email, role=Roles.User):
        self.username = username
        self.email = email
        self.role = role
        self.state = True
        self.date = dt.datetime.today()

    def save_to_db(self):
        if 0 < self.query.filter_by(username=self.username, state=True).count():
            raise Exception("Username already in use")
        elif 0 < self.query.filter_by(email=self.email, state=True).count():
            raise Exception("Email already in use")
        else:
            db.session.add(self)
            db.session.commit()

    def json(self, reviews=False):
        user = {"username": self.username,
                "email": self.email,
                "role": str(self.role)}
        if reviews:
            user['reviews'] = [review.json() for review in self.reviews]
        return user

    def delete_from_db(self):
        self.state = False
        db.session.commit()

    def update_password_from_db(self, password):
        self.hash_password(password)
        db.session.commit()

    def update_from_db(self, data):
        if 0 < self.query.filter_by(username=data['username'] and id != self.id, state=True).count():
            raise Exception("Username already in use")
        if 0 < self.query.filter_by(email=data['email'] and id != self.id, state=True).count():
            raise Exception("Email already in use")

        for attr, newValue in data.items():
            if newValue is not None:
                setattr(self, attr, newValue)
        db.session.commit()

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
        self.password = pwd_context.hash(password)

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
        return user.role.name
