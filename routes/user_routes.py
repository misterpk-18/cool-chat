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