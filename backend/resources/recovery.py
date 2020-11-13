from flask_restful import Resource

from model.recovery import PasswordRecoveryModel
from model.users import UsersModel


class PasswordRecovery(Resource):

    def get(self, key):
        recovery = PasswordRecoveryModel.find_by_key(key)
        if not recovery:
            return {"message": f"PasswordRecovery with ['key':{key}] is invalid"}, 404
        return {"user": UsersModel.find_by_id(recovery.user_id).json()}, 200
