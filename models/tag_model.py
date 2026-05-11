from database.db import get_connection
import psycopg2.extras
import uuid


class TagModel:

    @staticmethod
    def create_tag(tagname):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        tagid = str(uuid.uuid4())

        cursor.execute("""
            INSERT INTO tag(
                tagid,
                tagname
            )
            VALUES(%s,%s)
            RETURNING *
        """,(tagid,tagname))

        tag = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return tag

    @staticmethod
    def add_tag_to_post(
        postid,
        tagid
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO post_tag(
                postid,
                tagid
            )
            VALUES(%s,%s)
        """,(postid,tagid))

        conn.commit()

        cursor.close()
        conn.close()

        return True