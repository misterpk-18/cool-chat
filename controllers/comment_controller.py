from flask import request,jsonify
from models.comment_model import CommentModel


class CommentController:

    @staticmethod
    def add_comment():

        try:

            data = request.get_json()

            postid = data.get("postid")
            userid = data.get("userid")
            commtxt = data.get("commtxt")

            if not postid:
                return jsonify({
                    "success":False,
                    "message":"Postid is required"
                }),400

            if not userid:
                return jsonify({
                    "success":False,
                    "message":"Userid is required"
                }),400

            if not commtxt:
                return jsonify({
                    "success":False,
                    "message":"Comment text required"
                }),400

            comment = CommentModel.add_comment(
                postid,
                userid,
                commtxt
            )

            return jsonify({
                "success":True,
                "comment":comment
            }),201

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500

    @staticmethod
    def get_comments(postid):

        try:

            comments = CommentModel.get_comments_by_post(
                postid
            )

            return jsonify({
                "success":True,
                "comments":comments
            }),200

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500