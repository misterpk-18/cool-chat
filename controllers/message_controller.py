from flask import request, jsonify
from models.message_model import MessageModel

message_model = MessageModel()


class MessageController:

    def create_conversation(self):
        data = request.get_json()
        is_group = data.get("is_group", False)
        member_ids = data.get("member_ids", [])
        group_name = data.get("group_name", None)
        group_avatar = data.get("group_avatar", None)

        if len(member_ids) < 2:
            return jsonify({"error": "At least 2 members required"}), 400

        if not is_group:
            existing_id = message_model.find_dm_conversation(member_ids[0], member_ids[1])
            if existing_id:
                return jsonify({"conversation_id": existing_id, "existing": True}), 200

        conversation_id = message_model.create_conversation(is_group, group_name, group_avatar)

        for user_id in member_ids:
            message_model.add_member(conversation_id, user_id)

        return jsonify({"conversation_id": conversation_id, "existing": False}), 201

    def get_conversations(self, userid):
        conversations = message_model.get_user_conversations(userid)
        return jsonify({"conversations": conversations}), 200

    def get_messages(self, conversation_id):
        messages = message_model.get_conversation_messages(conversation_id)
        return jsonify({"messages": messages}), 200

    def send_message(self):
        data = request.get_json()
        conversation_id = data.get("conversation_id")
        sender_id = data.get("sender_id")
        content = data.get("content")
        media_url = data.get("media_url", None)

        if not conversation_id or not sender_id or not content:
            return jsonify({"error": "conversation_id, sender_id and content are required"}), 400

        result = message_model.save_message(conversation_id, sender_id, content, media_url)
        return jsonify({"message_id": result["id"], "created_at": result["created_at"]}), 201

    def mark_seen(self):
        data = request.get_json()
        conversation_id = data.get("conversation_id")
        user_id = data.get("user_id")

        if not conversation_id or not user_id:
            return jsonify({"error": "conversation_id and user_id are required"}), 400

        message_model.mark_seen(conversation_id, user_id)
        return jsonify({"success": True}), 200

    def get_members(self, conversation_id):
        members = message_model.get_conversation_members(conversation_id)
        return jsonify({"members": members}), 200

    def add_member(self):
        data = request.get_json()
        conversation_id = data.get("conversation_id")
        user_id = data.get("user_id")

        if not conversation_id or not user_id:
            return jsonify({"error": "conversation_id and user_id are required"}), 400

        message_model.add_member(conversation_id, user_id)
        return jsonify({"success": True}), 201