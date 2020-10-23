import datetime as dt

from db import db


class BooksModel(db.Model):
    __tablename__ = 'books'

    isbn = db.Column(db.Integer(), nullable=False, primary_key=True)
    vendible = db.Column(db.Boolean(), nullable=False)
    stock = db.Column(db.Integer(), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    titulo = db.Column(db.String(), nullable=False)
    autor = db.Column(db.String())
    editorial = db.Column(db.String())
    sinopsis = db.Column(db.String())
    fecha_de_publicacion = db.Column(db.DateTime(), nullable=False)

    def __init__(self, isbn, stock, precio, titulo, autor=None, editorial=None, sinopsis=None, fecha_de_publicacion=None):
        self.isbn = isbn
        self.vendible = True
        self.stock = stock
        self.precio = precio
        self.titulo = titulo
        self.autor = autor
        self.editorial = editorial
        self.sinopsis = sinopsis
        if fecha_de_publicacion is None:
            self.fecha_de_publicacion = dt.datetime.now()
        else:
            self.fecha_de_publicacion = fecha_de_publicacion
    def json(self):
        _ignore = self.isbn  # Forces execution to parse properly the class, fixing the bug of transient data
        atr = self.__dict__.copy()
        del atr["_sa_instance_state"]
        atr['fecha_de_publicacion'] = self.fecha_de_publicacion.strftime('%d-%m-%Y')
        return atr

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.vendible = False
        db.session.commit()

    def update_from_db(self, data):
        for key in data:
            setattr(self, key, data[key])
        db.session.commit()

    @classmethod
    def find_by_isbn(cls, isbn):
        return cls.query.filter_by(isbn=isbn).first()



