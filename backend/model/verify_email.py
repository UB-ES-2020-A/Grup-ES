import string
import random
from datetime import timedelta, datetime

from db import db
from utils.mail import send_email


class VerifyModel(db.Model):
    __tablename__ = 'verify_email'
    __table_args__ = (db.UniqueConstraint('key'),)

    SIZE = 32
    VALID_UNTIL = timedelta(hours=24)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    key = db.Column(db.String(SIZE), nullable=False)
    time = db.Column(db.DateTime(), nullable=False)
    confirmed_email = db.Column(db.Boolean(), nullable=False)

    def __init__(self, user_id, key=None):
        self.user_id = user_id
        self.time = datetime.now()
        self.key = self.generate_key() if key is None else key
        self.confirmed_email = False

    def json(self):
        return {'user_id': self.user_id,
                'valid_until': (self.time + self.VALID_UNTIL).strftime('%H:%M:%S')}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_from_db(self, data):
        for attr, newValue in data.items():
            if newValue is not None:
                setattr(self, attr, newValue)
        db.session.commit()

    def send_email(self, email, url_root):
        message = f"Gràcies per registrarte a BookShelter! Accedeix a {url_root}verify?key={self.key} "\
                  f"per confirmar el teu email. \n L'enllaç deixarà de ser vàlid en {self.VALID_UNTIL}"
        send_email(email, 'Verify your email', message)

    def has_time_expired(self):
        return self.time + self.VALID_UNTIL < datetime.now()

    @classmethod
    def find_by_id(cls, user_id):
        cls.clean_expired_keys()
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_key(cls, key):
        cls.clean_expired_keys()
        return cls.query.filter_by(key=key).first()

    @classmethod
    def clean_expired_keys(cls):
        """
        Cleans all entries that their time has expired. Will be called every time a query to the model is made.
        Expiration time is decided through constant class variable VALID_UNTIL.
        """
        time = datetime.now() - cls.VALID_UNTIL
        cls.query.filter(cls.time <= time).delete()

    @classmethod
    def generate_key(cls):
        """
        Generates a random key avoiding duplicating keys using the most secure random generator of the OS.
        The key will be made by a combination of uppercase and lowercase letters and numbers.
        """
        new_key = ''.join(
            random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(cls.SIZE))
        while cls.query.filter_by(key=new_key).count() != 0:
            new_key = ''.join(
                random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(cls.SIZE))
        return new_key

        new_key = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(cls.SIZE))
        dup = cls.find_by_key(new_key)
        while dup:
            new_key = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(cls.SIZE))
        return new_key

        # return 'asdfghjkl'
