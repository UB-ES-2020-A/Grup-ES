import random
import string
from datetime import datetime, timedelta

from db import db
from enum import Enum

from utils.mail import send_email


class PasswordRecoveryModel(db.Model):
    __tablename__ = 'password_recovery'
    __table_args__ = (db.UniqueConstraint('key'),)

    SIZE = 32
    VALID_UNTIL = timedelta(hours=1)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    key = db.Column(db.Integer(), nullable=False)
    time = db.Column(db.DateTime(), nullable=False)

    def __init__(self, user_id, key=None):
        self.user_id = user_id
        self.time = datetime.now()
        self.key = self.generate_key() if key is None else key

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
        """
        Updates through a dictionary with paris of string of name of attribute and it's value. Following same structure
        as json(). In case of wanting to modify an attribute of an enum use the string name of one of the values.

        Will raise Exception in case of invalid enum value if it isn't contained inside the possible values of the enum.
        """
        for attr, newValue in data.items():
            if newValue is not None:
                cls = getattr(self, attr)
                # Checks if value is of the attribute that's trying to be modified is an Enum
                if isinstance(cls, Enum):
                    # Checks if the enum doesn't contain the newValue
                    if newValue not in type(cls).__members__:
                        raise Exception(f"Enum {type(cls).__name__} doesn't have value: {newValue}")
                    # Gets the object of the enum with same name as newValue
                    setattr(self, attr, type(cls)[newValue])
                else:
                    setattr(self, attr, newValue)
        db.session.commit()

    def send_email(self, email, url_root):
        message = f"Has sol·licitat una recuperació de contrasenya. Accedeix a {url_root}change?key={self.key} "\
                  f"per canviar de contrasenya. \n L'enllaç deixarà de ser vàlid en {self.VALID_UNTIL} o si es torna " \
                  f"a solicitar un canvi en la mateixa compte."
        send_email(email, 'Password recovery', message)

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
        Cleans all entries that their time has expired. Will be called everytime a query to the model is made.
        Expiration time is decided through constant class variable VALID_UNTIL.
        """
        now = datetime.now()
        cls.query.filter(cls.time + cls.VALID_UNTIL >= now).delete()

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
