import datetime as dt

from flask_restful import Resource
from flask_restful import reqparse
from model.books import BooksModel

def parse_book():
    parser = reqparse.RequestParser()

    parser.add_argument('isbn', type=int, required=True,
                        help="In this field goes the isbn of the book, cannot be left blank")
    parser.add_argument('stock', type=int, required=True,
                        help="In this field goes the stock of the book, cannot be left blank")
    parser.add_argument('precio', type=float, required=True,
                        help="In this field goes the price of the book, cannot be left blank")
    parser.add_argument('titulo', type=str, required=True,
                        help="In this field goes the title of the book, cannot be left blank")
    parser.add_argument('autor', type=str, required=True,
                        help="In this field goes the author of the book, cannot be left blank")
    parser.add_argument('editorial', type=str, required=True,
                        help="In this field goes the editorial of the book, cannot be left blank")
    parser.add_argument('sinopsis', type=str, required=True,
                        help="In this field goes the sinopsis of the book, cannot be left blank")
                        help="In this field goes the date of the book in YYYY-MM-DD format, cannot be left blank")
    return parser.parse_args()

class Books(Resource):

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
            parser = reqparse.RequestParser()
            parser.add_argument('isbn', type=int, required=True,
                                help="In this field goes the isbn of the book, cannot be left blank")
            parser.add_argument('stock', type=int, required=True,
                                help="In this field goes the stock of the book, cannot be left blank")
            parser.add_argument('precio', type=float, required=True,
                                help="In this field goes the price of the book, cannot be left blank")
            parser.add_argument('titulo', type=str, required=True,
                                help="In this field goes the title of the book, cannot be left blank")
            parser.add_argument('autor', type=str, required=True,
                                help="In this field goes the author of the book, cannot be left blank")
            parser.add_argument('editorial', type=str, required=True,
                                help="In this field goes the editorial of the book, cannot be left blank")
            parser.add_argument('sinopsis', type=str, required=True,
                                help="In this field goes the sinopsis of the book, cannot be left blank")
            parser.add_argument('fecha_de_publicacion', type=str, required=True,
                                help="In this field goes the date of the book in YYYY-MM-DD format, cannot be left blank")
            data = parser.parse_args()
            book.isbn = data['isbn']
            book.stock = data['stock']
            book.precio = data['precio']
            book.titulo = data['titulo']
            book.autor = data['autor']
            book.editorial = data['editorial']
            book.sinopsis = data['sinopsis']
            date_string = data['fecha_de_publicacion']
            date_time_obj = dt.datetime.strptime(date_string, '%Y-%m-%d')
            book.fecha_de_publicacion = date_time_obj

            try:
                book.save_to_db()
                return {"book": book.json()}, 200
            except:
                return {"message": "Error a la hora d'editar un llibre a base de dades"}, 500
