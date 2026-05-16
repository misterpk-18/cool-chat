from flask_socketio import SocketIO, emit, join_room, leave_room
from models.message_model import MessageModel


class SocketEvents:

    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.message_model = MessageModel()
        self.register()

    def register(self):

        @self.socketio.on("connect")
        def handle_connect():
            print("Client connected")
            emit("connected", {"message": "Successfully connected to server"})

        @self.socketio.on("disconnect")
        def handle_disconnect():
            print("Client disconnected")

        @self.socketio.on("join_conversation")
        def handle_join(data):
            """
            Client sends: { conversation_id, user_id }
            """
            conversation_id = str(data.get("conversation_id"))
            user_id = data.get("user_id")

            join_room(conversation_id)
            self.message_model.mark_seen(conversation_id, user_id)

            emit("joined", {
                "conversation_id": conversation_id,
                "user_id": user_id
            }, room=conversation_id)

            print(f"User {user_id} joined conversation {conversation_id}")

        @self.socketio.on("leave_conversation")
        def handle_leave(data):
            """
            Client sends: { conversation_id, user_id }
            """
            conversation_id = str(data.get("conversation_id"))
            user_id = data.get("user_id")

            leave_room(conversation_id)

            emit("left", {
                "conversation_id": conversation_id,
                "user_id": user_id
            }, room=conversation_id)

            print(f"User {user_id} left conversation {conversation_id}")

        @self.socketio.on("send_message")
        def handle_send_message(data):
            conversation_id = data.get("conversation_id")
            sender_id = data.get("sender_id")
            content = data.get("content")
            media_url = data.get("media_url", None)

            if not conversation_id or not sender_id or not content:
                emit("error", {"message": "conversation_id, sender_id and content are required"})
                return

            result = self.message_model.save_message(conversation_id, sender_id, content, media_url)

            emit("new_message", {
                "message_id": result["id"],
                "conversation_id": conversation_id,
                "sender_id": sender_id,
                "username": result["username"],   # ← add this
                "content": content,
                "media_url": media_url,
                "created_at": result["created_at"]
            }, room=str(conversation_id))
        
        @self.socketio.on("typing")
        def handle_typing(data):
            """
            Client sends: { conversation_id, user_id, username }
            """
            conversation_id = str(data.get("conversation_id"))
            user_id = data.get("user_id")
            username = data.get("username")

            emit("user_typing", {
                "user_id": user_id,
                "username": username
            }, room=conversation_id, include_self=False)

        @self.socketio.on("stop_typing")
        def handle_stop_typing(data):
            """
            Client sends: { conversation_id, user_id }
            """
            conversation_id = str(data.get("conversation_id"))
            user_id = data.get("user_id")

            emit("user_stop_typing", {
                "user_id": user_id
            }, room=conversation_id, include_self=False)

        @self.socketio.on("message_seen")
        def handle_message_seen(data):
            """
            Client sends: { conversation_id, user_id }
            """
            conversation_id = str(data.get("conversation_id"))
            user_id = data.get("user_id")

            self.message_model.mark_seen(conversation_id, user_id)

            emit("seen_update", {
                "conversation_id": conversation_id,
                "user_id": user_id
            }, room=conversation_id, include_self=False)