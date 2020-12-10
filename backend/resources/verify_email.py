from flask_restful import Resource

from model.users import UsersModel
from model.verify_email import VerifyModel
from utils.lock import lock


class VerifyEmail(Resource):

    def post(self, key):
        with lock:
            verify = VerifyModel.find_by_key(key)
            if verify is None:
                return {"message": f"Verify email with ['key':{key}] is invalid"}, 404
            if verify.has_time_expired():
                return {"message": f"Password Recovery time has expired."}, 403
            user = UsersModel.find_by_id(verify.user_id)
            user.confirmed_email.confirmed_email = True
            return {"user": user.json()}, 200
