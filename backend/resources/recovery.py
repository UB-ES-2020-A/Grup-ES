from flask import request
from flask_restful import Resource, reqparse

from model.recovery import PasswordRecoveryModel
from model.users import UsersModel
from resources.users import check_constraints_user
from utils.lock import lock


def parse_data(required=False):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('email', required=not required, type=str, help="Password Recovery entry not valid: 'email' not provided")
    parser.add_argument('new_password', required=required, type=str,
                        help="Password Recovery entry not valid: 'new_password' not provided")
    return parser.parse_args()


class PasswordRecovery(Resource):

    def get(self, key):
        with lock:
            recovery = PasswordRecoveryModel.find_by_key(key)
            if recovery is None:
                return {"message": f"Password Recovery with ['key':{key}] is invalid"}, 404
            return {"user": UsersModel.find_by_id(recovery.user_id).json()}, 200

    def post(self):
        email = parse_data()['email']

        with lock:
            user = UsersModel.find_by_email(email)
            if user is None:
                return {"message": f"Password Recovery with ['email':{email}] is not found"}, 404

            recovery = PasswordRecoveryModel.find_by_id(user.id)
            if recovery is not None:
                try:
                    recovery.delete_from_db()
                except Exception as e:
                    return {"message": str(e)}, 500

            try:
                recovery = PasswordRecoveryModel(user.id)
                recovery.save_to_db()
            except Exception as e:
                return {"message": str(e)}, 500

        recovery.send_email(email, request.url_root)
        return {"recovery": recovery.json()}, 201

    def put(self, key):
        data = parse_data(True)
        check_constraints_user(data)

        with lock:
            recovery = PasswordRecoveryModel.find_by_key(key)
            if recovery is None:
                return {"message": f"Password Recovery with ['key':{key}] is invalid."}, 403

            if recovery.has_time_expired():
                return {"message": f"Password Recovery time has expired."}, 403

            user = UsersModel.find_by_id(recovery.user_id)
            if user is None:
                return {"message": f"User doesn't exist."}

            try:
                user.update_password_from_db(data['new_password'])
            except Exception as e:
                return {"message": str(e)}, 500

        return {"user": user.json()}, 200
