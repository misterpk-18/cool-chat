from flask import request,jsonify
from models.user_model import UserModel


class UserController:

    @staticmethod
    def update_profile():

        try:

            data = request.get_json()

            userid = data.get("userid")

            fullname = data.get(
                "fullname"
            )

            bio = data.get("bio")

            profpicurl = data.get(
                "profpicurl"
            )

            updated_user = UserModel.update_profile(
                userid,
                fullname,
                bio,
                profpicurl
            )

            return jsonify({
                "success":True,
                "user":updated_user
            }),200

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500