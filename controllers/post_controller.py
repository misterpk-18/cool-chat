from flask import request, jsonify
from models.post_model import PostModel


class PostController:

    @staticmethod
    def create_post():

        try:

            data = request.get_json()

            userid = data.get("userid")
            imageurl = data.get("imageurl")
            caption = data.get("caption")
            fullname = data.get("fullname")

            if not userid:
                return jsonify({
                    "success":False,
                    "message":"Userid is required"
                }),400

            if not imageurl:
                return jsonify({
                    "success":False,
                    "message":"Image url is required"
                }),400

            post = PostModel.create_post(
                userid,
                imageurl,
                caption,
                fullname
            )

            return jsonify({
                "success":True,
                "message":"Post created successfully",
                "post":post
            }),201

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500

    @staticmethod
    def get_all_posts():

        try:

            viewer = (
                request.args.get(
                    "viewer_userid"
                )
            )

            if viewer:

                posts = (
                    PostModel.get_all_posts_with_engagement(
                        viewer
                    )
                )

            else:

                posts = PostModel.get_all_posts()

            return jsonify({
                "success":True,
                "posts":posts
            }),200

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500

    @staticmethod
    def delete_post(postid):

        try:

            PostModel.delete_post(postid)

            return jsonify({
                "success":True,
                "message":"Post deleted successfully"
            }),200

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500