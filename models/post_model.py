from database.db import get_connection
import psycopg2.extras
import uuid


class PostModel:

    @staticmethod
    def create_post(
        userid,
        imageurl,
        caption,
        fullname
    ):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        postid = str(uuid.uuid4())

        cursor.execute("""
            INSERT INTO posts(
                postid,
                userid,
                imageurl,
                caption,
                fullname
            )
            VALUES(%s,%s,%s,%s,%s)
            RETURNING *
        """,(
            postid,
            userid,
            imageurl,
            caption,
            fullname
        ))

        post = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return post

    @staticmethod
    def get_all_posts():

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        cursor.execute("""
            SELECT *
            FROM posts
            ORDER BY createdat DESC
        """)

        posts = cursor.fetchall()

        cursor.close()
        conn.close()

        return posts

    @staticmethod
    def delete_post(postid):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM posts
            WHERE postid=%s
        """,(postid,))

        conn.commit()

        cursor.close()
        conn.close()

        return True