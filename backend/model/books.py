import datetime as dt

from db import db


class BooksModel(db.Model):
    __tablename__ = 'books'

    isbn = db.Column(db.BigInteger(), nullable=False, primary_key=True)
    vendible = db.Column(db.Boolean(), nullable=False)
    stock = db.Column(db.Integer(), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    titulo = db.Column(db.String(), nullable=False)
    autor = db.Column(db.String())
    editorial = db.Column(db.String())
    sinopsis = db.Column(db.String())
    url_imagen = db.Column(db.String())
    fecha_de_publicacion = db.Column(db.DateTime(), nullable=False)

    reviews = db.relationship('ReviewsModel', backref='book', lazy=True)
    score = db.relationship('ScoresModel', uselist=False, backref='book', lazy=True)

    def __init__(self, isbn, stock, precio, titulo, autor=None, editorial=None, sinopsis=None, url_imagen=None, fecha_de_publicacion=None):
        self.isbn = isbn
        self.vendible = True
        self.stock = stock
        self.precio = precio
        self.titulo = titulo
        self.autor = autor
        self.editorial = editorial
        self.sinopsis = sinopsis
        self.url_imagen = url_imagen
        if fecha_de_publicacion is None:
            self.fecha_de_publicacion = dt.datetime.now()
        else:
            self.fecha_de_publicacion = fecha_de_publicacion

    def json(self, reviews=False, score=False):
        _ignore = self.isbn  # Forces execution to parse properly the class, fixing the bug of transient data
        atr = self.__dict__.copy()
        del atr["_sa_instance_state"]
        atr['fecha_de_publicacion'] = self.fecha_de_publicacion.strftime('%Y-%m-%d')
        if reviews:
            reviews = self.reviews
            atr['reviews'] = [review.json() for review in reviews] if reviews else []
        if score:
            score = self.score
            atr['score'] = score.score if score else ''
        return atr

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.vendible = False
        db.session.commit()

    def update_from_db(self, data):
        for attr, newValue in data.items():
            if newValue is not None:
                setattr(self, attr, newValue)
        db.session.commit()

    @classmethod
    def find_by_isbn(cls, isbn):
        return cls.query.filter_by(isbn=isbn).first()



