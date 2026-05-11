from flask import request,jsonify


def auth_required(func):

    def wrapper(*args,**kwargs):

        userid = request.headers.get("userid")

        if not userid:

            return jsonify({
                "success":False,
                "message":"Authentication required"
            }),401

        return func(*args,**kwargs)

    wrapper.__name__ = func.__name__

    return wrapper