from flask import request,jsonify
from services.upload_service import UploadService


class UploadController:

    @staticmethod
    def upload_image():

        try:

            if "image" not in request.files:

                return jsonify({
                    "success":False,
                    "message":"No image uploaded"
                }),400

            image = request.files["image"]

            if image.filename == "":

                return jsonify({
                    "success":False,
                    "message":"Invalid image"
                }),400

            image_url = UploadService.upload_image(
                image
            )

            return jsonify({
                "success":True,
                "imageurl":image_url
            }),200

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500