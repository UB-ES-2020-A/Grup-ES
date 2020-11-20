from flask_restful import Resource, reqparse, abort
from flask import g
from model.users import UsersModel, auth, Roles
from model.library import LibraryModel, LibraryType, State
from model.books import BooksModel


def convert_option_to_enum(data):
    """
    Checks the validity of the parameters if the values, in case of being specified, sends an HTTP error 409.
    In case of values not being specified it default to:
        - library_type: Bought
        - state: Pending
    """
    if data['library_type'] is not None:
        if data['library_type'] not in LibraryType.__members__:
            abort(409, message={"message": f"Invalid type ['library_type': {data['library_type']} should be one of: {LibraryType.__members__}"})
        data['library_type'] = LibraryType[data['library_type']]
    else:
        data['library_type'] = LibraryType.Bought
    if 'state' in data:
        if data['state'] is not None:
            if data['state'] not in State.__members__:
                abort(409, message={"message": f"Invalid type ['state': {data['state']} should be one of: {State.__members__}"})
            data['state'] = State[data['state']]
        else:
            data['state'] = State.Pending if data['library_type'] == LibraryType.Bought else State.Nan
    return data


def parse_entry():
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('email', required=True, type=str, help="Library entry not valid: 'email' not provided")
    parser.add_argument('isbn', required=True, type=int, help="Library entry not valid: 'isbn' not provided")
    parser.add_argument('library_type', required=False, type=str)
    parser.add_argument('state', required=False, type=str)

    data = parser.parse_args()
    return convert_option_to_enum(data)


def parse_library_type():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('library_type', required=False, type=str)

    data = parser.parse_args()
    return convert_option_to_enum(data)['library_type']


class Library(Resource):

    @auth.login_required
    def get(self, email):
        user = UsersModel.find_by_email(email)
        if g.user != user:
            return {"message": "Invalid user to remove, can only be yourself"}, 401

        if not user:
            return {"message": f"User with ['email': {email}] Not Found"}, 404

        library_type = parse_library_type()

        library = LibraryModel.query.filter_by(user_id=user.id, library_type=library_type).all()
        return {"library": list(map(lambda entry: entry.json(), library))}, 200

    @auth.login_required
    def post(self):
        data = parse_entry()
        user = UsersModel.find_by_email(data['email'])
        if g.user != user:
            return {"message": "Invalid user to remove, can only be yourself"}, 401

        if not user:
            return {"message": f"User with ['email': {data['email']}] Not Found"}, 404

        if not BooksModel.find_by_isbn(data['isbn']):
            return {"message": f"Book with ['isbn': {data['isbn']}] Not Found"}, 404

        data['user_id'] = user.id
        del data['email']
        try:
            entry = LibraryModel(**data)
            entry.save_to_db()
        except Exception as e:
            return {"message": str(e)}, 500

        return entry.json(), 201


class LibraryVisibility(Resource):

    @staticmethod
    def check_keys(email, isbn):
        user = UsersModel.find_by_email(email)
        if user is None:
            abort(404, message={"message": f"User with ['email': {email}] Not Found"})

        if g.user != user:
            abort(401, message={"message": "Invalid user to remove, can only be yourself"})

        book = BooksModel.find_by_isbn(isbn)
        if book is None:
            abort(404, message={"message": f"Book with ['isbn': {isbn}] Not Found"})

        library = LibraryModel.find_by_id_and_isbn(user.id, isbn)
        if library is None:
            abort(404, message={"message": f"Entry with ['email': {email}, 'isbn': {isbn}] Not Found"})
        return library

    @auth.login_required
    def post(self, email, isbn):
        library = self.check_keys(email, isbn)

        if library.visible is True:
            return {"message": f"Entry with ['email': {email}, 'isbn': {isbn}] is already visible"}, 409

        try:
            library.change_visible_db(True)
        except Exception as e:
            return {"message": str(e)}, 500

        return {"message": f"Entry with ['email': {email}, 'isbn': {isbn}] has been made visible"}, 200

    @auth.login_required
    def delete(self, email, isbn):
        library = self.check_keys(email, isbn)

        if library.visible is False:
            return {"message": f"Entry with ['email': {email}, 'isbn': {isbn}] is already not visible"}, 409

        try:
            library.change_visible_db(False)
        except Exception as e:
            return {"message": str(e)}, 500

        return {"message": f"Entry with ['email': {email}, 'isbn': {isbn}] has been made not visible"}, 200
