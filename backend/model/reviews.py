from db import db

from model.books import BooksModel
from model.users import UsersModel


class ReviewsModel(db.Model):
    __tablename__ = 'reviews'

    isbn = db.Column(db.BigInteger(), db.ForeignKey('books.isbn'), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    score = db.Column(db.Integer(), nullable=False)
    review = db.Column(db.String())

    def __init__(self, isbn, user_id, score, review=None):
        self.isbn = isbn
        self.user_id = user_id
        self.score = score
        self.review = review

    def json(self):
        """
        Returns a dictionary with pairs of string of name of attribute and it's value.
        """
        atr = self.__dict__.copy()
        del atr["_sa_instance_state"]
        return atr

    def save_to_db(self):
        if ReviewsModel.query.get(self.isbn, self.user_id) is not None:
            raise Exception("Given user already posted a review. Did you meant to update it?")
        if UsersModel.find_by_id(self.user_id) is None:
            raise Exception("User with given id doesn't exist")
        if BooksModel.find_by_isbn(self.isbn) is None:
            raise Exception("Book with given isbn doesn't exist")
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        if UsersModel.find_by_id(self.user_id) is None:
            raise Exception("User with given id doesn't exist")
        if BooksModel.find_by_isbn(self.isbn) is None:
            raise Exception("Book with given isbn doesn't exist")
        if ReviewsModel.query.get(self.isbn, self.user_id) is None:
            raise Exception("Given user has no posted yet a review with given isbn.")
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_isbn_user_id(cls, isbn, user_id):
        return cls.query.get((isbn, user_id))

    @classmethod
    def find_by_isbn(cls, isbn):
        return cls.query.filter_by(isbn=isbn).all()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
