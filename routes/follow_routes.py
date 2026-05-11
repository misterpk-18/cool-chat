from flask import Blueprint
from controllers.follow_controller import FollowController


follow_bp = Blueprint(
    "follow_bp",
    __name__
)

follow_bp.route(
    "/follow-user",
    methods=["POST"]
)(
    FollowController.follow_user
)

follow_bp.route(
    "/unfollow-user",
    methods=["DELETE"]
)(
    FollowController.unfollow_user
)