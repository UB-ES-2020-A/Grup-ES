from flask_restful import Resource, reqparse, abort
from flask import g
from model.users import UsersModel, auth, Roles
from model.library import LibraryModel, LibraryType, State
from model.books import BooksModel
from model.reviews import ReviewsModel
from utils.lock import lock


def parse_review():
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('isbn', required=True, type=int,
                        help="ISBN of the book associated to the review. Can't be null.")
    parser.add_argument('email', required=True, type=str,
                        help="Email of the user associated to the review. Can't be null.")
    parser.add_argument('score', required=True, type=int,
                        help="Integer score ranging from 1 to 5 which indicates book score. Can't be null.")
    parser.add_argument('review', required=False, type=str,
                        help="Review message the user has posted with the score. Can be null.")

    return parser.parse_args()


class Reviews(Resource):

    @auth.login_required
    def post(self):
        data = parse_review()
        with lock:
            user = UsersModel.find_by_email(data['email'])
            if not user:
                return {"message": f"User with ['email': {data['email']}] Not Found"}, 404

            if g.user != user:
                return {"message": "Invalid user to remove, can only be yourself"}, 401

            if not BooksModel.find_by_isbn(data['isbn']):
                return {"message": f"Book with ['isbn': {data['isbn']}] Not Found"}, 404

            if data['score'] < 1 or data['score'] > 5:
                return {"message": f"{data['score']} is not a valid value for score. Score must be an integer ranging "
                                   f"from 1 to 5."}, 418

            if ReviewsModel.find_by_isbn_user_id(data.isbn, user.id) is not None:
                return {"message": "Given user already posted a review. Did you meant to update it?"}, 403

            data['user_id'] = user.id
            del data['email']
            try:
                review = ReviewsModel(**data)
                review.save_to_db()
            except Exception as e:
                return {"message": str(e)}, 500

        return review.json(), 201
