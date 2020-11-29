from flask_restful import Resource, reqparse
from flask import g
from model.users import UsersModel, auth
from utils.lock import lock


def parse_user(required_username=True):
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('username', required=required_username, type=str,
                        help="User not valid: 'username' not provided")
    parser.add_argument('email', required=True, type=str, help="User not valid: 'email' not provided")
    parser.add_argument('password', required=True, type=str, help="User not valid: 'password' not provided")

    return parser.parse_args()


def parse_modify_user():
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('username', required=False, type=str)
    parser.add_argument('email', required=False, type=str)
    parser.add_argument('new_password', required=False, type=str)
    parser.add_argument('password', required=True, type=str, help="You must enter the password in order to modify "
                                                                  "this field")
    return parser.parse_args()


def parse_reviews():
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('reviews', type=bool, required=False,
                        help="Indicates if returning the reviews of the book is needed.")
    return parser.parse_args()


class Users(Resource):

    def get(self, email):
        data = parse_reviews()
        with lock:
            user = UsersModel.find_by_email(email)
        if not user:
            return {"message": f"User with ['email':{email}] not found"}, 404

        return {"user": user.json(**data)}, 200

    def post(self):
        data = parse_user()
        with lock:
            user = UsersModel.find_by_username(data["username"])
            if user:
                return {"message": f"An user with same username {data['username']} already exists"}, 409
            user = UsersModel.find_by_email(data["email"])
            if user:
                return {"message": f"An user with same email {data['email']} already exists"}, 409

            password = data.pop("password")
            try:
                user = UsersModel(**data)
                user.hash_password(password)
                user.save_to_db()
            except Exception as e:
                return {"message": str(e)}, 500

        return user.json(), 201

    @auth.login_required
    def put(self, email):
        data = parse_modify_user()
        with lock:
            user = UsersModel.find_by_email(email)
            if not user:
                return {"message": f"User with ['email':{email}] not found"}, 404

            password = data.pop('password')
            if not user.check_password(password):
                return {'message': "Contrasenya incorrecta, torna a provar"}, 401
            if UsersModel.find_by_email(data['email']) is not None:
                return {"message": f"An user with same email {data['email']} already exists"}, 409
            if UsersModel.find_by_username(data['username']) is not None:
                return {"message": f"An user with same username {data['username']} already exists"}, 409
            new_password = data.pop('new_password')
            try:
                if new_password is not None:
                    user.hash_password(new_password)
                user.update_from_db(data)
            except Exception as e:
                return {"message": str(e)}, 500

        return {"user": user.json(), "token": user.generate_auth_token().decode('ascii')}, 200

    @auth.login_required
    def delete(self, email):
        with lock:
            user = UsersModel.find_by_email(email)

            if g.user != user:
                return {"message": "Invalid user to remove, can only be yourself"}, 401

            if not user:
                return {"message": f"User with ['email': {email}] Not Found"}, 404

            try:
                user.delete_from_db()
            except Exception as e:
                return {"message": str(e)}, 500

        return {"message": f"User with ['email': {email}] deleted"}, 200


class Login(Resource):

    def post(self):
        data = parse_user(False)

        with lock:
            account = UsersModel.find_by_email(data["email"])

            if not account:
                return {"message": "Invalid email"}, 404
            if not account.check_password(data["password"]):
                return {"message": "Invalid password"}, 400

            token = account.generate_auth_token()
        return {'token': token.decode('ascii')}, 200


class UsersList(Resource):

    def get(self):
        with lock:
            accounts = UsersModel.query.filter_by(state=True).all()
        return {"users": list(map(lambda account: account.json(), accounts)) if accounts else None}, 200
