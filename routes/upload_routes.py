from flask import Blueprint
from controllers.upload_controller import UploadController


upload_bp = Blueprint(
    "upload_bp",
    __name__
)

upload_bp.route(
    "/upload-image",
    methods=["POST"]
)(
    UploadController.upload_image
)