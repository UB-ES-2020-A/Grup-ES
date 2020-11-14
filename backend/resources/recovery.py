from flask import request
from flask_restful import Resource, reqparse

from model.recovery import PasswordRecoveryModel
from model.users import UsersModel


def parse_email():
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('email', required=True, type=str, help="Password Recovery entry not valid: 'email' not provided")

    return parser.parse_args()['email']


class PasswordRecovery(Resource):

    def get(self, key):
        recovery = PasswordRecoveryModel.find_by_key(key)
        if recovery is None:
            return {"message": f"PasswordRecovery with ['key':{key}] is invalid"}, 404
        return {"user": UsersModel.find_by_id(recovery.user_id).json()}, 200

    def post(self):
        email = parse_email()

        user = UsersModel.find_by_email(email)
        if user is None:
            return {"message": f"PasswordRecovery with ['email':{email}] is not found"}, 404

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
