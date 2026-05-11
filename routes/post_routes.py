from flask import Blueprint
from controllers.post_controller import PostController


post_bp = Blueprint(
    "post_bp",
    __name__
)

post_bp.route(
    "/posts",
    methods=["GET"]
)(
    PostController.get_all_posts
)

post_bp.route(
    "/create-post",
    methods=["POST"]
)(
    PostController.create_post
)

post_bp.route(
    "/delete-post/<postid>",
    methods=["DELETE"]
)(
    PostController.delete_post
)