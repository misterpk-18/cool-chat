import sys
import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

load_dotenv()

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from routes.auth_routes import auth_bp
from routes.post_routes import post_bp
from routes.comment_routes import comment_bp
from routes.like_routes import like_bp
from routes.follow_routes import follow_bp
from routes.user_routes import user_bp
from routes.upload_routes import upload_bp
from routes.message_routes import message_bp


app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "methods": [
                "GET",
                "POST",
                "PUT",
                "DELETE",
                "OPTIONS"
            ],
            "allow_headers": [
                "Content-Type",
                "Authorization"
            ]
        }
    }
)

# Initialize Socket.IO
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)


app.register_blueprint(auth_bp)
app.register_blueprint(post_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(like_bp)
app.register_blueprint(follow_bp)
app.register_blueprint(user_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(message_bp)


# Import socket events after socketio is initialized
from backend.socket_events import SocketEvents
SocketEvents(socketio)


if __name__ == "__main__":
    socketio.run(
        app,
        debug=True,
        port=5000,
        use_reloader=False
    )