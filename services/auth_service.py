import bcrypt
from models.user_model import UserModel


class AuthService:

    @staticmethod
    def signup_user(
        username,
        email,
        password,
        fullname,
        bio="",
        profpicurl=""
    ):

        existing_username = UserModel.get_user_by_username(
            username
        )

        if existing_username:

            return {
                "success":False,
                "message":"Username already exists"
            }

        existing_email = UserModel.get_user_by_email(
            email
        )

        if existing_email:

            return {
                "success":False,
                "message":"Email already exists"
            }

        user = UserModel.create_user(
            username,
            email,
            password,
            fullname,
            bio,
            profpicurl
        )

        return {
            "success":True,
            "user":user
        }

    @staticmethod
    def login_user(
        username_or_email,
        password
    ):

        user = UserModel.login_user(
            username_or_email,
            password
        )

        if not user:

            return {
                "success":False,
                "message":"Invalid credentials"
            }

        return {
            "success":True,
            "user":user
        }