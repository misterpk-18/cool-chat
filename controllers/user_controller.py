from flask import request,jsonify
from models.user_model import UserModel


class UserController:

    @staticmethod
    def update_profile():

        try:

            data = request.get_json()

            userid = data.get("userid")

            if not userid:

                return jsonify({
                    "success":False,
                    "message":"userid is required"
                }),400

            fullname = data.get(
                "fullname"
            )

            bio = data.get("bio")

            profpicurl = data.get(
                "profpicurl"
            )

            username_raw = data.get("username")

            if username_raw is None:

                existing = UserModel.get_user_by_id(
                    userid
                )

                if not existing:

                    return jsonify({
                        "success":False,
                        "message":"User not found"
                    }),404

                username = existing["username"]

            else:

                username = (
                    username_raw
                    if isinstance(username_raw, str)
                    else str(username_raw)
                ).strip()

                if not username:

                    return jsonify({
                        "success":False,
                        "message":"Username cannot be empty"
                    }),400

                taken = UserModel.get_user_by_username(
                    username
                )

                if taken and str(taken["userid"]) != str(userid):

                    return jsonify({
                        "success":False,
                        "message":"Username already taken"
                    }),409

            updated_user = UserModel.update_profile(
                userid,
                username,
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