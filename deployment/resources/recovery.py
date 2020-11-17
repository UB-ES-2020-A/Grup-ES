from flask import request
from flask_restful import Resource, reqparse

from model.recovery import PasswordRecoveryModel
from model.users import UsersModel


def parse_data(required=False):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, type=str, help="Password Recovery entry not valid: 'email' not provided")
    parser.add_argument('new_password', required=required, type=str,
                        help="Password Recovery entry not valid: 'new_password' not provided")
    return parser.parse_args()


class PasswordRecovery(Resource):

    def get(self, key):
        recovery = PasswordRecoveryModel.find_by_key(key)
        if recovery is None:
            return {"message": f"Password Recovery with ['key':{key}] is invalid"}, 404
        return {"user": UsersModel.find_by_id(recovery.user_id).json()}, 200

    def post(self):
        email = parse_data()['email']

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

        user = UsersModel.find_by_email(data['email'])
        if user is None:
            return {"message": f"Password Recovery with ['email':{data['email']}] is not found"}, 404

        recovery = PasswordRecoveryModel.find_by_id(user.id)
        if recovery is None:
            return {"message": f"Password Recovery with ['email':{data['email']}] not requested."}, 404

        if recovery.key != key:
            return {"message": f"Password Recovery with ['key':{key}] is invalid."}, 403

        if recovery.user_id != user.id:
            return {"message": f"Password Recovery attempting to modify password of other user."}, 403

        if recovery.has_time_expired():
            return {"message": f"Password Recovery time has expired."}, 403

        try:
            user.update_from_db(data['new_password'])
        except Exception as e:
            return {"message": str(e)}, 500

        return {"user": user.json()}, 200
