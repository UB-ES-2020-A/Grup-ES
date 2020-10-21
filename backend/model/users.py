from db import db
import datetime as dt
ROLES = ['manager','user']

class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String())
    role = db.Column(db.Enum(*ROLES), nullable=False)
    state = db.Column(db.Boolean(), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    def __init__(self, username, email, role, password):
        self.username = username
        self.email = email
        self.password = password
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

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def verify_password(self, password):
        return password == self.password

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def return_all(cls):
        return cls.query.all()