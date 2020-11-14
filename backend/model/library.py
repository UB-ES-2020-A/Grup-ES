from db import db
from enum import Enum

from model.books import BooksModel


class State(Enum):
    Pending = 1
    Reading = 2
    Finished = 3
    Dropped = 4


class LibraryType(Enum):
    Bought = 1
    WishList = 2


class LibraryModel(db.Model):
    __tablename__ = 'library'

    isbn = db.Column(db.BigInteger(), db.ForeignKey('books.isbn'), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    library_type = db.Column(db.Enum(LibraryType, name='library_types'), primary_key=True)
    state = db.Column(db.Enum(State, name='state_types'), nullable=False)
    visible = db.Column(db.Boolean(), nullable=False)

    def __init__(self, isbn, user_id, library_type=LibraryType.Bought, state=State.Pending):
        self.isbn = isbn
        self.user_id = user_id
        self.state = state
        self.visible = True
        self.library_type = library_type

    def json(self):
        """
        Returns a dictionary with paris of string of name of attribute and it's value. In case of Enum it just returns
        the name of the enum object (Enum.name).
        """
        _ignore = self.isbn  # Forces execution to parse properly the class, fixing the bug of transient data
        atr = self.__dict__.copy()
        atr['book'] = BooksModel.find_by_isbn(self.isbn).json()
        del atr['isbn']
        del atr["_sa_instance_state"]
        return {atr: value if not isinstance(value, Enum) else value.name for atr, value in atr.items()}

    def save_to_db(self):
        if BooksModel.find_by_isbn(self.isbn) is None:
            raise Exception("Book with isbn doesn't exist")
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.visible = False
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

    @classmethod
    def find_by_id_and_isbn(cls, user_id, isbn):
        return cls.query.filter_by(user_id=user_id, isbn=isbn).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()



