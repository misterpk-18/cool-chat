from flask import Blueprint
from controllers.auth_controller import AuthController


auth_bp = Blueprint(
    "auth_bp",
    __name__
)

auth_bp.route(
    "/signup",
    methods=["POST"]
)(
    AuthController.signup
)

auth_bp.route(
    "/login",
    methods=["POST"]
)(
    AuthController.login
)