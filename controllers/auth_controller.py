from flask import request,jsonify
from models.user_model import UserModel


class AuthController:

    @staticmethod
    def signup():

        try:

            data = request.get_json()
            print(request.get_json())

            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            fullname = data.get("fullname")
            bio = data.get("bio","")
            profpicurl = data.get("profpicurl","")

            if not username:
                return jsonify({
                    "success":False,
                    "message":"Username is required"
                }),400

            if not email:
                return jsonify({
                    "success":False,
                    "message":"Email is required"
                }),400

            if not password:
                return jsonify({
                    "success":False,
                    "message":"Password is required"
                }),400

            existing_username = UserModel.get_user_by_username(
                username
            )

            if existing_username:
                return jsonify({
                    "success":False,
                    "message":"Username already exists"
                }),409

            existing_email = UserModel.get_user_by_email(
                email
            )

            if existing_email:
                return jsonify({
                    "success":False,
                    "message":"Email already exists"
                }),409

            user = UserModel.create_user(
                username,
                email,
                password,
                fullname,
                bio,
                profpicurl
            )

            return jsonify({
                "success":True,
                "message":"Account created successfully",
                "user":user
            }),201

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500

    @staticmethod
    def login():

        try:

            data = request.get_json()

            username_or_email = data.get(
                "username_or_email"
            )

            password = data.get("password")

            if not username_or_email:
                return jsonify({
                    "success":False,
                    "message":"Username or email required"
                }),400

            if not password:
                return jsonify({
                    "success":False,
                    "message":"Password required"
                }),400

            user = UserModel.login_user(
                username_or_email,
                password
            )

            if not user:
                return jsonify({
                    "success":False,
                    "message":"Invalid credentials"
                }),401

            return jsonify({
                "success":True,
                "message":"Login successful",
                "user":user
            }),200

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500