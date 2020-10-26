from flask_restful import Resource
from flask_restful import reqparse
from model.books import BooksModel
from model.users import UsersModel, auth


class Books(Resource):
    @auth.login_required
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
            #type= DateTime()
            parser.add_argument('fecha_de_publicacion', type=int, required=True,
                                help="In this field goes the date of the book, cannot be left blank")
            return "Atributs del llibre canviats"
