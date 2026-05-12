from database.db import get_connection
import psycopg2.extras
import uuid


class LikeModel:

    @staticmethod
    def get_like(
        postid,
        userid
    ):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        cursor.execute("""
            SELECT *
            FROM likes
            WHERE postid=%s
            AND userid=%s
        """,(
            postid,
            userid
        ))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row

    @staticmethod
    def like_post(postid,userid):

        existing = LikeModel.get_like(
            postid,
            userid
        )

        if existing:

            return existing

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        likeid = str(uuid.uuid4())

        cursor.execute("""
            INSERT INTO likes(
                likeid,
                postid,
                userid
            )
            VALUES(%s,%s,%s)
            RETURNING *
        """,(
            likeid,
            postid,
            userid
        ))

        like = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return like

    @staticmethod
    def unlike_post(postid,userid):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM likes
            WHERE postid=%s
            AND userid=%s
        """,(postid,userid))

        conn.commit()

        cursor.close()
        conn.close()

        return True