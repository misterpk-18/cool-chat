from flask import request,jsonify
from models.follow_model import FollowModel


class FollowController:

    @staticmethod
    def follow_user():

        try:

            data = request.get_json()

            followerid = data.get("followerid")
            followeeid = data.get("followeeid")

            if not followerid:
                return jsonify({
                    "success":False,
                    "message":"Followerid required"
                }),400

            if not followeeid:
                return jsonify({
                    "success":False,
                    "message":"Followeeid required"
                }),400

            follow = FollowModel.follow_user(
                followerid,
                followeeid
            )

            return jsonify({
                "success":True,
                "follow":follow
            }),201

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500

    @staticmethod
    def unfollow_user():

        try:

            data = request.get_json()

            followerid = data.get("followerid")
            followeeid = data.get("followeeid")

            FollowModel.unfollow_user(
                followerid,
                followeeid
            )

            return jsonify({
                "success":True,
                "message":"User unfollowed"
            }),200

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500

    @staticmethod
    def get_follower_count():

        try:

            data = request.get_json()

            followeeid = data.get("followeeid")

            count = FollowModel.get_follower_count(followeeid)

            return jsonify({
                "success":True,
                "count":count
            }),200

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500

    @staticmethod
    def check_follow():

        try:

            data = request.get_json()

            followerid = data.get("followerid")
            followeeid = data.get("followeeid")

            is_following = FollowModel.check_follow(
                followerid,
                followeeid
            )

            return jsonify({
                "success":True,
                "is_following":is_following
            }),200

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500
        
    @staticmethod
    def get_following_count():

        try:

            data = request.get_json()

            followerid = data.get("followerid")

            count = FollowModel.get_following_count(followerid)

            return jsonify({
                "success":True,
                "count":count
            }),200

        except Exception as e:

            return jsonify({
                "success":False,
                "message":str(e)
            }),500 
