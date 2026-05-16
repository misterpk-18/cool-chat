from flask import Blueprint
from controllers.message_controller import MessageController

message_bp = Blueprint("message", __name__)
message_controller = MessageController()

# Conversations
message_bp.route("/conversations/create", methods=["POST"])(message_controller.create_conversation)
message_bp.route("/conversations/<userid>", methods=["GET"])(message_controller.get_conversations)
message_bp.route("/conversations/<int:conversation_id>/messages", methods=["GET"])(message_controller.get_messages)
message_bp.route("/conversations/<int:conversation_id>/members", methods=["GET"])(message_controller.get_members)

# Messages
message_bp.route("/conversations/send", methods=["POST"])(message_controller.send_message)
message_bp.route("/conversations/seen", methods=["PUT"])(message_controller.mark_seen)
message_bp.route("/conversations/add-member", methods=["POST"])(message_controller.add_member)