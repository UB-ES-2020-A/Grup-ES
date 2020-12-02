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


def check_user_and_book(user_model, isbn):
    if not user_model:
        abort(404, message={"message": f"User Not Found"})

    if not BooksModel.find_by_isbn(isbn):
        abort(404, message={"message": f"Book with ['isbn': {isbn}] Not Found"})

    if g.user != user_model:
        abort(401, message={"message": "Invalid user to remove, can only be yourself"})


class Reviews(Resource):

    @auth.login_required
    def post(self):
        data = parse_review()
        with lock:
            user = UsersModel.find_by_email(data['email'])
            check_user_and_book(user, data['isbn'])

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

    @auth.login_required(role=Roles.User.name)
    def delete(self, user_id, isbn):
        with lock:
            user = UsersModel.find_by_id(user_id)
            check_user_and_book(user, isbn)

            review = ReviewsModel.find_by_isbn_user_id(isbn, user_id)
            if review is None:
                return {"message": "Given user hasn't posted a review yet. Did you meant to post it?"}, 404

            try:
                review.delete_from_db()
            except Exception as e:
                return {"message": str(e)}, 500

        return {"message": f"Review with ['user_id': {user_id}, 'isbn': {isbn}] deleted"}, 200

