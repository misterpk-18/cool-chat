from flask import request,jsonify
from models.like_model import LikeModel


class LikeController:

    @staticmethod
    def like_post():

        try:

            data = request.get_json()

            postid = data.get("postid")
            userid = data.get("userid")

            if not postid:
                return jsonify({
                    "success":False,
                    "message":"Postid required"
                }),400

            if not userid:
                return jsonify({
                    "success":False,
                    "message":"Userid required"
                }),400

            like = LikeModel.like_post(
                postid,
                userid
            )

            return jsonify({
                "success":True,
                "like":like
            }),201

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500

    @staticmethod
    def unlike_post():

        try:

            data = request.get_json()

            postid = data.get("postid")
            userid = data.get("userid")

            if not postid:
                return jsonify({
                    "success":False,
                    "message":"Postid required"
                }),400

            if not userid:
                return jsonify({
                    "success":False,
                    "message":"Userid required"
                }),400

            LikeModel.unlike_post(
                postid,
                userid
            )

            return jsonify({
                "success":True,
                "message":"Post unliked"
            }),200

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500