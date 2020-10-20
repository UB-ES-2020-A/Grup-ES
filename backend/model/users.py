from db import db

class UsersModel(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(), primary_key=True)
    email = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())
    role = db.Column(db.String())
    state = db.Column(db.Boolean())

    def __init__(self, username, email, role, password):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.state = True

    def __repr__(self):
        return f"<{self.username}-{self.email}-{self.role}>"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def verify_password(self, password):
        return password == self.password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def return_all(cls):
        return cls.query.all()