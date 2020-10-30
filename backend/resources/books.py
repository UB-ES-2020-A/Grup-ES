import datetime as dt

from flask_restful import Resource
from flask_restful import reqparse
from sqlalchemy import desc, asc

from model.books import BooksModel


def parse_book(minimal=False):
    str_variable = "" if minimal else ", cannot be left blank"
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('isbn', type=int, required=not minimal,
                        help="In this field goes the isbn of the book" + str_variable)
    parser.add_argument('stock', type=int, required=not minimal,
                        help="In this field goes the stock of the book" + str_variable)
    parser.add_argument('precio', type=float, required=not minimal,
                        help="In this field goes the price of the book" + str_variable)
    parser.add_argument('titulo', type=str, required=not minimal,
                        help="In this field goes the title of the book" + str_variable)
    parser.add_argument('autor', type=str, required=False,
                        help="In this field goes the author of the book")
    parser.add_argument('editorial', type=str, required=False,
                        help="In this field goes the editorial of the book")
    parser.add_argument('sinopsis', type=str, required=False,
                        help="In this field goes the sinopsis of the book")
    parser.add_argument('url_imagen', type=str, required=False,
                        help="In this field goes the url of the image associated to the book")
    parser.add_argument('fecha_de_publicacion', type=str, required=False,
                        help="In this field goes the date of the book in YYYY-MM-DD format")
    data = parser.parse_args()
    if data["fecha_de_publicacion"] is not None:
        data["fecha_de_publicacion"] = dt.datetime.strptime(data["fecha_de_publicacion"], '%Y-%m-%d')

    return data


class Books(Resource):

    def get(self, isbn):
        book = BooksModel.find_by_isbn(isbn)
        if not book:
            return {"message": f"Book with ['isbn':{isbn}] not found"}, 404
        return {"book": book.json()}, 200

    def post(self):
        data = parse_book()
        book = BooksModel.find_by_isbn(data["isbn"])
        if book:
            return {"message": f"A book with same isbn {data['isbn']} already exists"}, 409
        try:
            book = BooksModel(**data)
            book.save_to_db()
        except Exception as e:
            return {"message": str(e)}, 500

        return book.json(), 201

    def put(self, isbn):
        book = BooksModel.find_by_isbn(isbn)
        if book is None:
            return {"message": "Book with ['isbn': " + str(isbn) + "] Not Found"}, 404
        else:
            data = parse_book(minimal=True)
            for key in data:
                if data[key] is not None:
                    setattr(book, key, data[key])
            try:
                book.save_to_db()
                return {"book": book.json()}, 200
            except Exception as e:
                print(str(e))
                return {"message": "Error a la hora d'editar un llibre a base de dades"}, 500

    def delete(self, isbn):
        book = BooksModel.find_by_isbn(isbn)

        if book is None:
            return {"message": f"Book with ['isbn': {isbn}] Not Found"}, 404

        if not book.vendible:
            return {"message": f"Book with ['isbn': {isbn}] was previously removed"}, 409

        try:
            book.delete_from_db()
        except Exception as e:
            return {"message": str(e)}, 500

        return {"message": f"Book with ['isbn': {isbn}] deleted"}, 200


class BooksList(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument('numBooks', type=int, required=False,
                            help="In this field goes the number of the books to show")
        parser.add_argument('param', type=str, required=False,
                            help="In this field goes the param you want to order")
        parser.add_argument('order', type=str, required=False,
                            help="In this field goes the order (asc, desc) of what you would like to show")
        data = parser.parse_args()
        if data['param'] is None:
            books = BooksModel.query.limit(data['numBooks']).all()
        else:
            if data['order'] == "asc":
                books = BooksModel.query.order_by(asc(data['param'])).limit(data['numBooks']).all()
            else:
                books = BooksModel.query.order_by(desc(data['param'])).limit(data['numBooks']).all()
        return {'books': [book.json() for book in books]}, 200
