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

follow_bp.route(
    "/follower-count",
    methods=["POST"]
)(
    FollowController.get_follower_count
)

follow_bp.route(
    "/following-count",
    methods=["POST"]
)(
    FollowController.get_following_count
)

follow_bp.route(
    "/check-follow",
    methods=["POST"]
)(
    FollowController.check_follow
)