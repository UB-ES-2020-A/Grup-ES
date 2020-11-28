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
            abort(409, message={"message": f"Invalid type ['library_type': {data['library_type']} should be one of: "
                                           f"{LibraryType.__members__}"})
        data['library_type'] = LibraryType[data['library_type']]
    else:
        data['library_type'] = LibraryType.Bought
    if 'state' in data:
        if data['state'] is not None:
            if data['state'] not in State.__members__:
                abort(409, message={"message": f"Invalid type ['state': {data['state']} should be one of: "
                                               f"{State.__members__}"})
            data['state'] = State[data['state']]
        else:
            data['state'] = State.Pending if data['library_type'] == LibraryType.Bought else State.Nan
    return data


def parse_entry(requiered=True):
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('isbn', required=requiered, type=int, help="Library entry not valid: 'isbn' not provided")
    parser.add_argument('library_type', required=False, type=str)
    parser.add_argument('state', required=False, type=str)

    data = parser.parse_args()
    return convert_option_to_enum(data) if requiered else data


def parse_library_type():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('library_type', required=False, type=str)

    data = parser.parse_args()
    return convert_option_to_enum(data)['library_type']


def check_user(email):
    user = UsersModel.find_by_email(email)
    if user is None:
        abort(404, message={"message": f"User with ['email': {email}] Not Found"})

    if g.user != user:
        abort(401, message={"message": "Invalid user to remove, can only be yourself"})
    return user


def check_keys(email, isbn):
    user = check_user(email)

    book = BooksModel.find_by_isbn(isbn)
    if book is None:
        abort(404, message={"message": f"Book with ['isbn': {isbn}] Not Found"})

    library = LibraryModel.find_by_id_and_isbn(user.id, isbn)
    if library is None:
        abort(404, message={"message": f"Entry with ['email': {email}, 'isbn': {isbn}] Not Found"})
    return library


class Library(Resource):

    @auth.login_required
    def get(self, email):
        user = check_user(email)

        library_type = parse_library_type()

        library = LibraryModel.query.filter_by(user_id=user.id, library_type=library_type).all()
        return {"library": list(map(lambda entry: entry.json(), library))}, 200


class LibraryEntry(Resource):

    @auth.login_required
    def post(self, email):
        data = parse_entry()
        user = check_user(email)

        if not BooksModel.find_by_isbn(data['isbn']):
            return {"message": f"Book with ['isbn': {data['isbn']}] Not Found"}, 404

        data['user_id'] = user.id
        try:
            entry = LibraryModel(**data)
            entry.save_to_db()
        except Exception as e:
            return {"message": str(e)}, 500

        return entry.json(), 201

    @auth.login_required
    def put(self, email, isbn):
        library = check_keys(email, isbn)
        data = parse_entry(False)

        del data['isbn']
        try:
            library.update_from_db(data)
        except Exception as e:
            return {"message": str(e)}, 500

        return {"message": f"Entry with ['email': {email}, 'isbn': {isbn}] has been made visible"}, 200


class LibraryVisibility(Resource):

    @auth.login_required
    def post(self, email, isbn):
        library = check_keys(email, isbn)

        if library.visible is True:
            return {"message": f"Entry with ['email': {email}, 'isbn': {isbn}] is already visible"}, 409

        try:
            library.change_visible_db(True)
        except Exception as e:
            return {"message": str(e)}, 500

        return {"message": f"Entry with ['email': {email}, 'isbn': {isbn}] has been made visible"}, 200

    @auth.login_required
    def delete(self, email, isbn):
        library = check_keys(email, isbn)

        if library.visible is False:
            return {"message": f"Entry with ['email': {email}, 'isbn': {isbn}] is already not visible"}, 409

        try:
            library.change_visible_db(False)
        except Exception as e:
            return {"message": str(e)}, 500

        return {"message": f"Entry with ['email': {email}, 'isbn': {isbn}] has been made not visible"}, 200
