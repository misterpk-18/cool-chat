from database.db import get_connection
import psycopg2.extras
import uuid


class CommentModel:

    @staticmethod
    def add_comment(
        postid,
        userid,
        commtxt
    ):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        comid = str(uuid.uuid4())

        cursor.execute("""
            INSERT INTO comments(
                comid,
                postid,
                userid,
                commtxt
            )
            VALUES(%s,%s,%s,%s)
            RETURNING *
        """,(
            comid,
            postid,
            userid,
            commtxt
        ))

        comment = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return comment

    @staticmethod
    def get_comments_by_post(postid):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        cursor.execute("""
            SELECT *
            FROM comments
            WHERE postid=%s
            ORDER BY createdat ASC
        """,(postid,))

        comments = cursor.fetchall()

        cursor.close()
        conn.close()

        return comments