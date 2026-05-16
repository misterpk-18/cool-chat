from database.db import get_connection


class MessageModel:

    def create_conversation(self, is_group=False, group_name=None, group_avatar=None):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO conversations (is_group, group_name, group_avatar)
            VALUES (%s, %s, %s) RETURNING id
            """,
            (is_group, group_name, group_avatar)
        )
        conversation_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return conversation_id

    def add_member(self, conversation_id, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO conversation_members (conversation_id, user_id)
            VALUES (%s, %s) ON CONFLICT DO NOTHING
            """,
            (conversation_id, user_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    def get_user_conversations(self, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT c.id, c.is_group, c.group_name, c.group_avatar, c.created_at
            FROM conversations c
            JOIN conversation_members cm ON c.id = cm.conversation_id
            WHERE cm.user_id = %s
            ORDER BY c.created_at DESC
            """,
            (user_id,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {
                "id": row[0],
                "is_group": row[1],
                "group_name": row[2],
                "group_avatar": row[3],
                "created_at": str(row[4])
            }
            for row in rows
        ]

    def get_conversation_messages(self, conversation_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT m.id, m.sender_id, u.username, m.content, m.media_url, m.seen_by, m.created_at
            FROM messages m
            JOIN users u ON m.sender_id = u.userid
            WHERE m.conversation_id = %s
            ORDER BY m.created_at ASC
            """,
            (conversation_id,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {
                "id": row[0],
                "sender_id": row[1],
                "username": row[2],
                "content": row[3],
                "media_url": row[4],
                "seen_by": row[5],
                "created_at": str(row[6])
            }
            for row in rows
        ]

    def save_message(self, conversation_id, sender_id, content, media_url=None):

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO messages (conversation_id, sender_id, content, media_url)
            VALUES (%s, %s, %s, %s) RETURNING id, created_at
            """,
            (conversation_id, sender_id, content, media_url)
        )
        row = cur.fetchone()
        conn.commit()

        # Fetch username
        cur.execute("SELECT username FROM users WHERE userid = %s", (sender_id,))
        user = cur.fetchone()

        cur.close()
        conn.close()
        return {
            "id": row[0],
            "created_at": str(row[1]),
            "username": user[0] if user else sender_id
        }

    def mark_seen(self, conversation_id, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE messages
            SET seen_by = array_append(seen_by, %s)
            WHERE conversation_id = %s AND NOT (%s = ANY(seen_by))
            """,
            (user_id, conversation_id, user_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    def get_conversation_members(self, conversation_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT u.userid, u.username
            FROM conversation_members cm
            JOIN users u ON cm.user_id = u.userid
            WHERE cm.conversation_id = %s
            """,
            (conversation_id,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"userid": row[0], "username": row[1]} for row in rows]

    def find_dm_conversation(self, user1_id, user2_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT c.id FROM conversations c
            JOIN conversation_members cm1 ON c.id = cm1.conversation_id AND cm1.user_id = %s
            JOIN conversation_members cm2 ON c.id = cm2.conversation_id AND cm2.user_id = %s
            WHERE c.is_group = FALSE
            LIMIT 1
            """,
            (user1_id, user2_id)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row[0] if row else None