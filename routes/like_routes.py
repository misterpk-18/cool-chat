from flask import Blueprint
from controllers.like_controller import LikeController


like_bp = Blueprint(
    "like_bp",
    __name__
)

like_bp.route(
    "/like-post",
    methods=["POST"]
)(
    LikeController.like_post
)

like_bp.route(
    "/unlike-post",
    methods=["DELETE"]
)(
    LikeController.unlike_post
)