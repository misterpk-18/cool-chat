from flask import Blueprint
from controllers.user_controller import UserController


user_bp = Blueprint(
    "user_bp",
    __name__
)

user_bp.route(
    "/update-profile",
    methods=["PUT"]
)(
    UserController.update_profile
)

user_bp.route(
    "/search-users",
    methods=["GET"]
)(
    UserController.search_users
)

user_bp.route(
    "/user/<userid>",
    methods=["GET"]
)(
    UserController.get_public_profile
)