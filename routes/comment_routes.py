from flask import Blueprint 
from controllers.comment_controller import CommentController 

comment_bp=Blueprint(
    "comment_bp",
    __name__
)

comment_bp.route(
    "/add-comment",
    methods=["POST"]
)(
    CommentController.add_comment
)

comment_bp.route(
    "/get-comments/<postid>",
    methods=["GET"]
)(
    CommentController.get_comments
)